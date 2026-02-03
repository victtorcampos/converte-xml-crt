from lxml import etree

class XMLConverter:
    def __init__(self, tree, picms, csosn_900_cst, target_crt):
        self.tree = tree
        self.picms = float(picms)
        self.csosn_900_cst = csosn_900_cst
        self.target_crt = str(target_crt)
        self.ns = {
            'nfe': 'http://www.portalfiscal.inf.br/nfe',
            'ds': 'http://www.w3.org/2000/09/xmldsig#'
        }
        self.total_vBC = 0
        self.total_vICMS = 0
        self.total_vProd = 0
        self.total_vNF = 0
        self.original_crt = self._get_current_crt()
        self.signature_removed = False
        self.protnfe_removed = False

    def _get_current_crt(self):
        crt_element = self.tree.find('.//nfe:emit/nfe:CRT', self.ns)
        return crt_element.text if crt_element is not None else None

    def convert(self):
        self._remove_unwanted_elements()

        report = {
            'original_crt': self.original_crt,
            'target_crt': self.target_crt,
            'signature_removed': self.signature_removed,
            'protnfe_removed': self.protnfe_removed,
            'status': 'ERRO'
        }

        if self.target_crt == '1' and self.original_crt == '1':
            report['status'] = 'IGNORADO'
            return None, report

        self._update_emitter_crt()
        
        if self.original_crt == '1':
            self._process_items()
            self._update_totals()

        report['status'] = 'CONVERTIDO'
        xml_bytes = etree.tostring(self.tree, pretty_print=True, encoding='UTF-8', xml_declaration=True)
        return xml_bytes, report

    def _remove_unwanted_elements(self):
        signatures = self.tree.findall('.//ds:Signature', self.ns)
        if signatures:
            self.signature_removed = True
            for sig in signatures:
                sig.getparent().remove(sig)
        
        protnfes = self.tree.findall('.//nfe:protNFe', self.ns)
        if protnfes:
            self.protnfe_removed = True
            for prot in protnfes:
                prot.getparent().remove(prot)

    def _update_emitter_crt(self):
        crt_element = self.tree.find('.//nfe:emit/nfe:CRT', self.ns)
        if crt_element is not None:
            crt_element.text = self.target_crt

    def _process_items(self):
        items = self.tree.findall('.//nfe:det', self.ns)
        for det in items:
            icms_element = det.find('./nfe:imposto/nfe:ICMS', self.ns)
            icms_sn_element = icms_element.find('./*', self.ns)
            if icms_sn_element is not None and 'ICMSSN' in icms_sn_element.tag:
                csosn = icms_sn_element.find('nfe:CSOSN', self.ns).text
                self._convert_icms(icms_element, csosn, det, icms_sn_element)
    
    def _convert_icms(self, icms, csosn, det, icms_sn):
        orig = icms_sn.find('nfe:orig', self.ns).text
        icms.remove(icms_sn)

        conversion_map = {
            '101': self._create_cst_00,
            '102': self._create_cst_00,
            '103': self._create_cst_00,
            '300': self._create_cst_41,
            '400': self._create_cst_41,
            '201': self._create_cst_10,
            '202': self._create_cst_60,
            '203': self._create_cst_60,
            '500': self._create_cst_60,
            '900': self._create_cst_900,
        }

        conversion_func = conversion_map.get(csosn)
        if conversion_func:
            conversion_func(icms, det, orig)
    
    def _get_det_values(self, det):
        def get_value(tag):
            element = det.find(f".//nfe:prod/nfe:{tag}", self.ns)
            return float(element.text) if element is not None and element.text is not None else 0.0

        v_prod = get_value('vProd')
        v_frete = get_value('vFrete')
        v_seg = get_value('vSeg')
        v_outro = get_value('vOutro')
        v_desc = get_value('vDesc')
        return v_prod, v_frete, v_seg, v_outro, v_desc

    def _create_cst_00(self, icms, det, orig):
        v_prod, v_frete, v_seg, v_outro, v_desc = self._get_det_values(det)
        v_bc = v_prod + v_frete + v_seg + v_outro - v_desc
        v_icms = v_bc * (self.picms / 100)

        self.total_vBC += v_bc
        self.total_vICMS += v_icms

        icms_00 = etree.SubElement(icms, etree.QName(self.ns['nfe'], 'ICMS00'))
        etree.SubElement(icms_00, etree.QName(self.ns['nfe'], 'orig')).text = orig
        etree.SubElement(icms_00, etree.QName(self.ns['nfe'], 'CST')).text = '00'
        etree.SubElement(icms_00, etree.QName(self.ns['nfe'], 'modBC')).text = '3'
        etree.SubElement(icms_00, etree.QName(self.ns['nfe'], 'vBC')).text = f'{v_bc:.2f}'
        etree.SubElement(icms_00, etree.QName(self.ns['nfe'], 'pICMS')).text = f'{self.picms:.2f}'
        etree.SubElement(icms_00, etree.QName(self.ns['nfe'], 'vICMS')).text = f'{v_icms:.2f}'
    
    def _create_cst_10(self, icms, det, orig):
        pass

    def _create_cst_41(self, icms, det, orig):
        icms_40 = etree.SubElement(icms, etree.QName(self.ns['nfe'], 'ICMS40'))
        etree.SubElement(icms_40, etree.QName(self.ns['nfe'], 'orig')).text = orig
        etree.SubElement(icms_40, etree.QName(self.ns['nfe'], 'CST')).text = '41'

    def _create_cst_60(self, icms, det, orig):
        icms_60 = etree.SubElement(icms, etree.QName(self.ns['nfe'], 'ICMS60'))
        etree.SubElement(icms_60, etree.QName(self.ns['nfe'], 'orig')).text = orig
        etree.SubElement(icms_60, etree.QName(self.ns['nfe'], 'CST')).text = '60'
        etree.SubElement(icms_60, etree.QName(self.ns['nfe'], 'vBCSTRet')).text = '0.00'
        etree.SubElement(icms_60, etree.QName(self.ns['nfe'], 'vICMSSTRet')).text = '0.00'

    def _create_cst_900(self, icms, det, orig):
        cst = self.csosn_900_cst
        if cst == '90':
            icms_90 = etree.SubElement(icms, etree.QName(self.ns['nfe'], 'ICMS90'))
            etree.SubElement(icms_90, etree.QName(self.ns['nfe'], 'orig')).text = orig
            etree.SubElement(icms_90, etree.QName(self.ns['nfe'], 'CST')).text = cst
            etree.SubElement(icms_90, etree.QName(self.ns['nfe'], 'modBC')).text = '3'
            etree.SubElement(icms_90, etree.QName(self.ns['nfe'], 'vBC')).text = '0.00'
            etree.SubElement(icms_90, etree.QName(self.ns['nfe'], 'pICMS')).text = '0.00'
            etree.SubElement(icms_90, etree.QName(self.ns['nfe'], 'vICMS')).text = '0.00'

    def _update_totals(self):
        items = self.tree.findall('.//nfe:det', self.ns)
        total_v_prod = sum(self._get_det_values(det)[0] for det in items)
        
        icms_tot = self.tree.find('.//nfe:ICMSTot', self.ns)
        if icms_tot is not None:
            vBC_element = icms_tot.find('nfe:vBC', self.ns)
            if vBC_element is not None: vBC_element.text = f'{self.total_vBC:.2f}'
            
            vICMS_element = icms_tot.find('nfe:vICMS', self.ns)
            if vICMS_element is not None: vICMS_element.text = f'{self.total_vICMS:.2f}'

            vICMSDeson_element = icms_tot.find('nfe:vICMSDeson', self.ns)
            if vICMSDeson_element is not None: vICMSDeson_element.text = '0.00'

            vProd_element = icms_tot.find('nfe:vProd', self.ns)
            if vProd_element is not None: vProd_element.text = f'{total_v_prod:.2f}'
            
            v_desc = float(icms_tot.find('nfe:vDesc', self.ns).text or 0)
            v_st = float(icms_tot.find('nfe:vST', self.ns).text or 0)
            v_frete = float(icms_tot.find('nfe:vFrete', self.ns).text or 0)
            v_seg = float(icms_tot.find('nfe:vSeg', self.ns).text or 0)
            v_outro = float(icms_tot.find('nfe:vOutro', self.ns).text or 0)
            v_ipi = float(icms_tot.find('nfe:vIPI', self.ns).text or 0)

            v_nf = total_v_prod - v_desc + v_st + v_frete + v_seg + v_outro + v_ipi
            
            vNF_element = icms_tot.find('nfe:vNF', self.ns)
            if vNF_element is not None: vNF_element.text = f'{v_nf:.2f}'
