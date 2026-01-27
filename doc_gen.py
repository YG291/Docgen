from docx import Document
from docx.text.run import Run
from docx.text.paragraph import Paragraph
from docx.table import Table
from pathlib import Path

class Doc:
    """Representation of a generic document.
    """
    
    def __init__(self, name: str, to_replace: dict[str, str]) -> None:
        self.doc = Document(name)
        self.to_replace = to_replace

    def _replace_in_run(self, r: Run, old: str, new: str) -> None:
        """Helper method that replaces every instance of old in r.text with new.
        """
        r.text = r.text.replace(old, new)

    def _replace_p(self, p: Paragraph, key: str) -> None:
        """Helper method that fixes every fragmented run in p and replaces every instance 
        of key with its corresponding value in self.to_replace.
        """
        while key in p.text:
            start_index = p.text.find(key)
            end_index = start_index + len(key)
            current = 0
            _runs = []
            for r in p.runs:
                if current < end_index and current + len(r.text) >= start_index:
                    _runs.append(r)
                current += len(r.text)
                if current > end_index:
                    break
            for r_index in range(len(_runs)):
                if r_index != 0: 
                    _runs[0].text = _runs[0].text + _runs[r_index].text
                    _runs[r_index].text = ''
            if _runs:
               self._replace_in_run(_runs[0], key, self.to_replace[key])

    def replace_main(self) -> None:
        for key in self.to_replace:
            for p in self.doc.paragraphs:
                self._replace_p(p, key)

    def _replace_t(self, t: Table, key) -> None:
        """Helper method to replace paragraphs in tables.
        """
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    self._replace_p(p, key)

    def replace_tables(self) -> None:
        for key in self.to_replace:
            for t in self.doc.tables:
                self._replace_t(t, key)
        
    def replace_hf(self) -> None:
        for s in self.doc.sections:
            for p in s.footer.paragraphs:
                for key in self.to_replace:
                    self._replace_p(p, key)
            for t in s.footer.tables:
                for key in self.to_replace:    
                    self._replace_t(t, key)
            for p in s.first_page_footer.paragraphs:
                for key in self.to_replace:
                    self._replace_p(p, key)
            for t in s.first_page_footer.tables:
                for key in self.to_replace:
                    self._replace_t(t, key)
            for p in s.header.paragraphs:
                for key in self.to_replace:
                    self._replace_p(p, key)
            for t in s.header.tables:
                for key in self.to_replace:
                    self._replace_t(t, key)


if __name__ == '__main__':
    main_path = Path(__file__).parent
    doc_path = main_path / "templates" / "Stock Purchase Agreement" / "SPA.docx"
    test = Doc(doc_path, {"[CORP]": "JACKSON & JEFFERSON INC.", "[BUYER]": "Jacob Jackson", "[PRICE]": "500", "[CEO]": "Jacob Jefferson", "[COUNT]": "50,000"})
    test.replace_main()
    test.replace_tables()
    test.replace_hf()
    test.doc.save(doc_path.parent.parent.parent / "output" / "SPA_filled.docx")


#test.doc.paragraphs[0].runs[0] OR test.doc.paragraphs[0].runs[0].text
#test.doc.tables[0].rows[0].cells[0].paragraphs[0].text