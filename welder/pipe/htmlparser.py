from welder.node import Pipe
import bs4


class HTMLParser(Pipe):
    def __init__(self, label: str, drop_HTML=False) -> None:
        super().__init__(label, inputs=[str, list], outputs=[str, list] if not drop_HTML else [list])
        self.drop_HTML = drop_HTML


class HTMLContext2Lines(HTMLParser):

    def __init__(self, label: str, drop_HTML=False) -> None:
        super().__init__(label, drop_HTML=drop_HTML)


    def pipe(self):
        HTML = self.values[0]
        lines = self.values[1]

        soup = bs4.BeautifulSoup(HTML, 'html.parser')
        body = soup.body
        try:
            body.find('div',class_='MMM--disclaimerBlock').decompose()
            body.find('div',class_='formContainer').decompose()
            body.find('nav',class_='m-nav').decompose()
            body.find('div',class_='m-footer').decompose()
            body.find('div',class_='MMM--skipMenu').decompose()
        except:
            pass
            # print("did not find disclaimer or formcontainer while cleaning")
        more_lines = self.extract_lines(body)
        lines.extend(more_lines)

        return [HTML, lines] if not self.drop_HTML else [lines]


    def extract_lines(self, body):
        lines = []
        def recursive_extract(tag):

            if isinstance(tag, bs4.element.Tag):
                for t in tag.children:
                    recursive_extract(t)
            else:
                text = tag.text
                lines.append(text)

        if body: recursive_extract(body)

        return lines

class HTMLTable2Lines(HTMLParser):

    def __init__(self, label: str, drop_HTML=False) -> None:
        super().__init__(label, drop_HTML=drop_HTML)
        '''
        This pipe extracts the tables out of the HTML text passed by the scraper.
        It does not categorize the data using a classifier.
        It appends the table into the context lines by normalizong into sentences.
        '''


    def pipe(self):
        HTML = self.values[0]
        lines = self.values[1]
        
        tlines = []
        data, label = self.get_rc(HTML)
        for d, l in zip(data, label):
            tlines.append(f"The product's {l} is {d}")
        lines.extend(tlines)
        
        return [HTML, lines] if not self.drop_HTML else [lines]


    def get_rc(self, HTML):
        row, col = [], []
        try:
            soup = bs4.BeautifulSoup(HTML, "html.parser")
            table = soup.find_all("tr", class_="MMM--dat-row")
            for item in table[1:]:
                c, r = [x for x in item.text.split("\n") if x]
                row.append(r)
                col.append(c)

        except Exception as err:
            pass
        return row, col