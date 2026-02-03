from lxml import etree

class XMLConverter:
    def __init__(self, tree, picms, csosn_900_cst):
        self.tree = tree
        self.picms = float(picms)
        self.csosn_900_cst = csosn_900_cst
        self.ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        self.total_vBC = 0
        self.total_vICMS = 0
        self.total_vProd = 0
        self.total_vNF = 0

    def convert(self):
        """Executa o processo de conversão e retorna o XML como uma string de bytes."""
        self._update_emitter_crt()
        self._process_items()
        self._update_totals()
        # Serializa para bytes usando UTF-8, o que é compatível com a declaração XML.
        return etree.tostring(self.tree, pretty_print=True, encoding='UTF-8', xml_declaration=True)

    def _update_emitter_crt(self):
        """Altera o CRT do emitente para 3 (Regime Normal)."""
        crt_element = self.tree.find('.//nfe:emit/nfe:CRT', self.ns)
        if crt_element is not None:
            crt_element.text = '3'

    def _process_items(self):
        """Processa cada item (det) da NFe."""
        items = self.tree.findall('.//nfe:det', self.ns)
        for det in items:
            icms_element = det.find('./nfe:imposto/nfe:ICMS', self.ns)
            icms_sn_element = icms_element.find('./*', self.ns) # Pega o primeiro filho (ICMSSN*)
            if icms_sn_element is not None:
                csosn = icms_sn_element.find('nfe:CSOSN', self.ns).text
                self._convert_icms(icms_element, csosn, det, icms_sn_element)
    
    def _convert_icms(self, icms, csosn, det, icms_sn):
        """Converte o grupo de ICMS baseado no CSOSN."""
        orig = icms_sn.find('nfe:orig', self.ns).text
        icms.remove(icms_sn)

        conversion_map = {
            '101': self._create_cst_00,
            '102': self._create_cst_41,
            '103': self._create_cst_41, # Regra idêntica ao 102
            '300': self._create_cst_41, # Regra idêntica ao 102
            '400': self._create_cst_41, # Regra idêntica ao 102
            '201': self._create_cst_10,
            '202': self._create_cst_60,
            '203': self._create_cst_60, # Regra idêntica ao 202
            '500': self._create_cst_60,
            '900': self._create_cst_900,
        }

        conversion_func = conversion_map.get(csosn)
        if conversion_func:
            conversion_func(icms, det, orig)
    
    def _get_det_values(self, det):
        """Função auxiliar para obter valores de um item, tratando campos ausentes."""
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

        icms_00 = etree.SubElement(icms, 'ICMS00')
        etree.SubElement(icms_00, 'orig').text = orig
        etree.SubElement(icms_00, 'CST').text = '00'
        etree.SubElement(icms_00, 'modBC').text = '3'
        etree.SubElement(icms_00, 'vBC').text = f'{v_bc:.2f}'
        etree.SubElement(icms_00, 'pICMS').text = f'{self.picms:.2f}'
        etree.SubElement(icms_00, 'vICMS').text = f'{v_icms:.2f}'
    
    def _create_cst_10(self, icms, det, orig):
        # Implementação para CST 10 (com ST)
        pass

    def _create_cst_41(self, icms, det, orig):
        icms_40 = etree.SubElement(icms, 'ICMS40') # Grupo para CST 40, 41, 50
        etree.SubElement(icms_40, 'orig').text = orig
        etree.SubElement(icms_40, 'CST').text = '41'
        # Não há campos de valor ou desoneração para CST 41

    def _create_cst_60(self, icms, det, orig):
        # Implementação para CST 60 (ICMS cobrado anteriormente por ST)
        icms_60 = etree.SubElement(icms, 'ICMS60')
        etree.SubElement(icms_60, 'orig').text = orig
        etree.SubElement(icms_60, 'CST').text = '60'
        # Normalmente, vBCSTRet e vICMSSTRet viriam da nota original,
        # mas para a conversão, podemos zerá-los se não houver lógica específica.
        etree.SubElement(icms_60, 'vBCSTRet').text = '0.00'
        etree.SubElement(icms_60, 'vICMSSTRet').text = '0.00'

    def _create_cst_900(self, icms, det, orig):
        # Usa o CST customizável (90 por padrão)
        cst = self.csosn_900_cst
        if cst == '90':
            icms_90 = etree.SubElement(icms, 'ICMS90')
            etree.SubElement(icms_90, 'orig').text = orig
            etree.SubElement(icms_90, 'CST').text = cst
            etree.SubElement(icms_90, 'modBC').text = '3' # Valor da operação
            etree.SubElement(icms_90, 'vBC').text = '0.00' # Outras bases de cálculo
            etree.SubElement(icms_90, 'pICMS').text = '0.00'
            etree.SubElement(icms_90, 'vICMS').text = '0.00'
        # Adicionar lógica para outros CSTs se necessário

    def _update_totals(self):
        """Atualiza o bloco ICMSTot com os valores calculados."""
        items = self.tree.findall('.//nfe:det', self.ns)
        total_v_prod = sum(self._get_det_values(det)[0] for det in items)
        # Adicione outras somas (frete, seguro, etc.) se necessário

        icms_tot = self.tree.find('.//nfe:ICMSTot', self.ns)
        if icms_tot is not None:
            icms_tot.find('nfe:vBC', self.ns).text = f'{self.total_vBC:.2f}'
            icms_tot.find('nfe:vICMS', self.ns).text = f'{self.total_vICMS:.2f}'
            icms_tot.find('nfe:vProd', self.ns).text = f'{total_v_prod:.2f}'
            
            # Recalcula vNF com base nos novos totais
            v_nf = total_v_prod - float(icms_tot.find('nfe:vDesc', self.ns).text or 0) \
                   + float(icms_tot.find('nfe:vST', self.ns).text or 0) \
                   + float(icms_tot.find('nfe:vFrete', self.ns).text or 0) \
                   + float(icms_tot.find('nfe:vSeg', self.ns).text or 0) \
                   + float(icms_tot.find('nfe:vOutro', self.ns).text or 0) \
                   + float(icms_tot.find('nfe:vIPI', self.ns).text or 0)

            icms_tot.find('nfe:vNF', self.ns).text = f'{v_nf:.2f}'
