import pytest
from lxml import etree as ET
from app.core.conversion import XMLConverter

# Namespace da NFe, essencial para encontrar os elementos
NS = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

@pytest.fixture
def base_xml_tree():
    """Carrega a árvore XML base a partir do arquivo para cada teste."""
    with open('tests/base_simples.xml', 'rb') as f:
        return ET.parse(f)

def test_csosn_101_to_cst_00(base_xml_tree):
    """Testa a conversão de CSOSN 101 para CST 00."""
    # Modifica o XML para o cenário de teste
    det = base_xml_tree.find(".//nfe:det[@nItem='1']", NS)
    icms_sn = det.find(".//nfe:ICMSSN101", NS)
    icms_sn.tag = 'ICMSSN101' # Garante que o cenário é 101
    icms_sn.find("nfe:CSOSN", NS).text = '101'
    
    # Executa o conversor
    converter = XMLConverter(tree=base_xml_tree, picms=18.0, csosn_900_cst='90')
    converted_tree_str = converter.convert()
    converted_tree = ET.fromstring(converted_tree_str)

    # Busca o novo grupo de ICMS
    icms_group = converted_tree.find(".//nfe:det[@nItem='1']//nfe:ICMS00", NS)
    assert icms_group is not None, "O grupo ICMS00 não foi encontrado."
    
    # Valida os campos
    assert icms_group.find('nfe:CST', NS).text == '00'
    assert icms_group.find('nfe:modBC', NS).text == '3'
    assert float(icms_group.find('nfe:vBC', NS).text) == 100.00
    assert float(icms_group.find('nfe:pICMS', NS).text) == 18.0
    assert float(icms_group.find('nfe:vICMS', NS).text) == 18.0

def test_csosn_102_to_cst_41(base_xml_tree):
    """Testa a conversão de CSOSN 102 para CST 41."""
    det = base_xml_tree.find(".//nfe:det[@nItem='1']", NS)
    # Substitui o grupo de imposto
    imposto = det.find(".//nfe:imposto", NS)
    icms = imposto.find(".//nfe:ICMS", NS)
    icms.getparent().remove(icms)
    new_icms = ET.fromstring("""
        <ICMS xmlns='http://www.portalfiscal.inf.br/nfe'>
            <ICMSSN102>
                <orig>0</orig>
                <CSOSN>102</CSOSN>
            </ICMSSN102>
        </ICMS>
    """)
    imposto.append(new_icms)

    # Executa a conversão
    converter = XMLConverter(tree=base_xml_tree, picms=17.0, csosn_900_cst='90')
    converted_tree_str = converter.convert()
    converted_tree = ET.fromstring(converted_tree_str)

    # Valida a conversão
    icms_group = converted_tree.find(".//nfe:det[@nItem='1']//nfe:ICMS40", NS)
    assert icms_group is not None
    assert icms_group.find('nfe:CST', NS).text == '41'
    assert icms_group.find('nfe:vICMSDeson', NS) is None # Campo não deve existir
    assert icms_group.find('nfe:motDesICMS', NS) is None

# ... (outros testes para 202, 500, 900, etc.)

def test_crt_update(base_xml_tree):
    """Testa se o CRT do emitente é atualizado para 3."""
    converter = XMLConverter(tree=base_xml_tree, picms=17.0, csosn_900_cst='90')
    converted_tree_str = converter.convert()
    converted_tree = ET.fromstring(converted_tree_str)

    crt_element = converted_tree.find(".//nfe:emit/nfe:CRT", NS)
    assert crt_element.text == '3'

def test_totals_recalculation(base_xml_tree):
    """Testa se o bloco ICMSTot é recalculado corretamente."""
    # Adiciona um segundo produto para um cálculo mais complexo
    infNFe = base_xml_tree.find(".//nfe:infNFe", NS)
    det1 = base_xml_tree.find(".//nfe:det[@nItem='1']", NS)
    det2 = ET.fromstring(ET.tostring(det1)) # Clona o primeiro produto
    det2.set('nItem', '2')
    det2.find(".//nfe:vProd", NS).text = "50.00"
    infNFe.insert(infNFe.index(det1) + 1, det2)

    # Roda a conversão
    converter = XMLConverter(tree=base_xml_tree, picms=20.0, csosn_900_cst='90')
    converted_tree_str = converter.convert()
    converted_tree = ET.fromstring(converted_tree_str)

    # Valida os totais
    icms_tot = converted_tree.find(".//nfe:ICMSTot", NS)
    assert float(icms_tot.find('nfe:vBC', NS).text) == 150.00
    assert float(icms_tot.find('nfe:vICMS', NS).text) == 30.00 # 100*0.20 + 50*0.20
    assert float(icms_tot.find('nfe:vProd', NS).text) == 150.00
    assert float(icms_tot.find('nfe:vNF', NS).text) == 150.00

def test_conversion_with_specific_file():
    """Testa a conversão usando um arquivo XML real fornecido."""
    file_path = 'tests/51260123593075000129550010000041811000047514_v4.00-procNFe.xml'
    with open(file_path, 'rb') as f:
        specific_xml_tree = ET.parse(f)
    
    # Executa o conversor com uma alíquota de ICMS de exemplo e CST 90 para CSOSN 900
    converter = XMLConverter(tree=specific_xml_tree, picms=18.0, csosn_900_cst='90')
    converted_tree_bytes = converter.convert()
    
    # Analisa o resultado
    converted_tree = ET.fromstring(converted_tree_bytes)
    
    # Valida se o CRT foi alterado
    crt_element = converted_tree.find(".//nfe:emit/nfe:CRT", NS)
    assert crt_element is not None
    assert crt_element.text == '3'
    
    # Adicione outras asserções aqui se souber o resultado esperado
    # Por exemplo, verificar se um CSOSN 102 virou CST 41
