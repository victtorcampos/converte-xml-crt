import pytest
from lxml import etree
from app.core.conversion import XMLConverter

@pytest.fixture
def xml_with_protocol_content():
    with open("tests/fixture_with_protocol.xml", "rb") as f:
        return f.read()

@pytest.fixture
def base_simples_content():
    with open("tests/base_simples.xml", "rb") as f:
        return f.read()

# Teste para verificar se a assinatura e o protocolo são removidos
def test_removes_signature_and_protocol(xml_with_protocol_content):
    tree = etree.fromstring(xml_with_protocol_content)
    converter = XMLConverter(tree, picms=18.0, csosn_900_cst='90', target_crt=2)
    
    converted_xml, report = converter.convert()
    
    assert converted_xml is not None
    assert report['signature_removed'] is True
    assert report['protnfe_removed'] is True

    # Verificar se os elementos não existem mais no XML convertido
    converted_tree = etree.fromstring(converted_xml)
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    assert converted_tree.find('.//nfe:Signature', ns) is None
    assert converted_tree.find('.//nfe:protNFe', ns) is None

# Teste para a regra de ignorar a conversão se o CRT de origem e destino são 1
def test_ignore_rule_crt1_to_crt1(base_simples_content):
    tree = etree.fromstring(base_simples_content)
    converter = XMLConverter(tree, picms=18.0, csosn_900_cst='90', target_crt=1)
    
    converted_xml, report = converter.convert()
    
    assert converted_xml is None
    assert report['status'] == 'IGNORADO'

# Teste para garantir que a conversão ocorra quando o CRT de destino é diferente
def test_conversion_crt1_to_crt2(base_simples_content):
    tree = etree.fromstring(base_simples_content)
    converter = XMLConverter(tree, picms=18.0, csosn_900_cst='90', target_crt=2)
    
    converted_xml, report = converter.convert()
    
    assert converted_xml is not None
    assert report['status'] == 'CONVERTIDO'
    
    converted_tree = etree.fromstring(converted_xml)
    ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    crt_element = converted_tree.find('.//nfe:emit/nfe:CRT', ns)
    assert crt_element.text == '2'
