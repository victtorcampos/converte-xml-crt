from lxml import etree

class XMLValidator:
    def __init__(self, file_content):
        self.file_content = file_content
        self.tree = self._parse_xml()

    def _parse_xml(self):
        try:
            return etree.fromstring(self.file_content)
        except etree.XMLSyntaxError as e:
            raise ValueError(f"XML malformado: {e}")

    def validate(self):
        self._validate_namespace()
        self._validate_root_tag()
        self._validate_model()
        self._validate_crt()

    def _validate_namespace(self):
        if "http://www.portalfiscal.inf.br/nfe" not in self.tree.nsmap.values():
            raise ValueError("Namespace NFe não encontrado.")

    def _validate_root_tag(self):
        if self.tree.tag not in [f"{{{self.tree.nsmap[None]}}}nfeProc", f"{{{self.tree.nsmap[None]}}}NFe"]:
            raise ValueError("Tag raiz inválida.")

    def _validate_model(self):
        mod_element = self.tree.find(".//{*}mod")
        if mod_element is None or mod_element.text not in ["55", "65"]:
            raise ValueError("Modelo de documento inválido.")

    def _validate_crt(self):
        crt_element = self.tree.find(".//{*}CRT")
        if crt_element is None or crt_element.text != "1":
            raise ValueError("CRT de origem inválido.")
