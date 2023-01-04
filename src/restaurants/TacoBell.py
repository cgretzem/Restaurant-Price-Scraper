from Restaurant import Restaurant
import asyncio
import time
import bs4
import xmltodict
import json
class TacoBell(Restaurant):
    def __init__(self, address, driver):
        super().__init__(address)
        self.driver = driver
        self.availProducts = {
                'Crunchy Taco': 'Crunchy Taco',
                'Nacho Cheese Doritos® Locos Tacos':'Doritos Locos Tacos',
                'Chalupa Supreme®':'Chalupa Supreme - Beef',
                'Cheesy Gordita Crunch':'Cheesy Gordita Crunch - Beef',
                'Bean Burrito':'Bean Burrito',
                'Cheesy Bean and Rice Burrito': 'Cheese Bean Rice Burrito',
                'Burrito Supreme®':'Burrito Supreme - Beef',
                'Nachos BellGrande®':'Nachos Bell Grande',
                'Chicken Quesadilla':'Chicken Quesadilla',
                'Steak Quesadilla':'Steak Quesadilla',
                'Cheese Quesadilla' : 'Cheese Quesadilla',
                'Chicken Chipotle Melt' : 'Chicken Chipotle Melt',
                '3 Crunchy Tacos Combo' : '3 Crunchy Tacos Combo (Large)',
                'Burrito Supreme® Combo' : 'Burrito Supreme Combo (Large)',
                'Reduced-Fat Sour Cream' : 'Sour Cream',
                'Guacamole' : 'Guacamole',
                'Pepsi®' : 'Fountain Drink',
                'Chipotle Sauce' : 'Chipotle Sauce',
        }

    def default_menu(self):
        menu = {}
        for product in self.availProducts.values():
            if "Drink" not in product:
                menu[product] = -1
        menu["Small Fountain Drink"] = -1
        menu["Medium Fountain Drink"] = -1
        menu["Large Fountain Drink"] = -1
        return menu



    async def get_page(self, url):
        self.driver.get(url)
        soup = bs4.BeautifulSoup(self.driver.page_source, features="lxml")
        try:
            found = soup.find('pre').text
            return json.loads(found)
        except:
            xml = soup.find('storefindersearchpage')
            return xmltodict.parse(str(xml))

    
    async def scrape_menu(self):
        if self.store_num == None:
            return
        url = f"https://www.tacobell.com/tacobellwebservices/v2/tacobell/products/menu/{self.store_num}"

        payload={}
        headers = {
        'authority': 'www.tacobell.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'bm_sz=F91828A36FBD67DAC661F456625B0A60~YAAQh6XcF8rjvAuFAQAAEz6vcBK0aeuZJh2G46/v6WQEvAYZv7UxhzRNAw5PDibhCAkRWoaSBf+11Cev08ZVOgeJS3Y28G/K7Eyk2Ng3IjOSRhRKop54pkbRh4Kpf+F96idFM9I82wgQa7/TIp18o5CEQWJbyhoEdXPIcHUalm1ZRM2aqDjmGd0xXoJhyWnIMvfRsW8dvn9rj/j01bw1A+VaSoj3IPVhfMGHDVIiNiVknc3g0NOTBaaXUIxq9Qj+boPUPp/8muTi6j+k64e7P8J3USBJALKmVoVizSReziNRjhJPMg==~4277826~3158840; _gcl_au=1.1.1489476549.1672632812; AWSELB=3119AFC114622B4A1B853AE9C5E9EE3FDC77CA92FED3D79EF26C5E0E7BB0BFC7A17127F169063CAD7A343484FD805257476DC3A0AB39AAF919B41CC9DBE6DF861DF2761C26; AWSELBCORS=3119AFC114622B4A1B853AE9C5E9EE3FDC77CA92FED3D79EF26C5E0E7BB0BFC7A17127F169063CAD7A343484FD805257476DC3A0AB39AAF919B41CC9DBE6DF861DF2761C26; _cs_c=0; _gid=GA1.2.1320616382.1672632813; ak_bmsc=3E7729A3259C5E7FD083921AF5952303~000000000000000000000000000000~YAAQh6XcFzrkvAuFAQAAnEavcBIFwwl8zGZOifQVOGlID9Z3ugHMCXrBmP2n01RYFNGXpEewuJkJlB9AUSwj8JqBKSCNIpz4p/xhmJbqjIuVklPFPcByUlEPURrhpo7/VgpCheqmWficDEeTMzcvd8wWMmdDokn/YLJKFx1/+AYYoNZynY/K5YpZ9hSwnQt0z+GDUYsZZPL8tKhB+6fbBN83/ZzEZ0nfyo5iSWNCfoqBP75M4K+HyVGXNoYbFlq7+03oHBkT9CFa5UrutmgPUrxuyBXrCzZOS2Hpycdf5xng8lrs6AJekvZTq5kwomed3i6CJcvZshp+SvxdPfaJkQVth7iKzjKG9Qj7QJuzipZMbFR8uE3BIqIT+W27vmzJRxbHoucAO5jP3WbxbI57HQPJxjOXTc7i2ehLFDhmjZMMWPqvnUeft+T1+e6WZvELQGhK5sqR3p9U9ycT5HCPd+J9N+6ombXFYktJ9dv5npQqf30XnTax/1ep69/Y; AMP_MKTG_7601ffc7c9=JTdCJTIycmVmZXJyZXIlMjIlM0ElMjJodHRwcyUzQSUyRiUyRnd3dy5nb29nbGUuY29tJTJGJTIyJTJDJTIycmVmZXJyaW5nX2RvbWFpbiUyMiUzQSUyMnd3dy5nb29nbGUuY29tJTIyJTdE; _cs_cvars=%7B%7D; _cs_mk=0.5404754101141898_1672638157137; JSESSIONID=8EFA23E582735599BC5DAA1CA750A799; CSRFToken=2ee64573-4fd5-434a-bd7a-ea2f4bd57a60; _cs_id=b80f64be-2e87-a27f-9ce6-fb1a40e44645.1672632812.2.1672638167.1672635485.1625591181.1706796812955; _cs_s=12.0.0.1672639967843; _ga_81J1R64GQ6=GS1.1.1672635487.2.1.1672638257.60.0.0; _abck=C2FB400344A2CAAEC831E10FA4A42D02~-1~YAAQlaXcFwvAKhmFAQAAq1oCcQlK/V6MRwVDl4SIH5u0bG3ES4I7Ix6fMN2KOS0KVCAwVhjtWz6X6y+3UCExerZ7MTiJuDhAGkLoaxLoi5JwiuiX/uPMDdaPmguhLqNTknWZx1O/F3rXoG8k7tb/AOSLrxsylPT4ieNlafWFt+0Z8laqRg3NV4mEYa7RPLQx1tJ7wJaU0JNIZQyG9PGkoENP7nOwvWuFvslTiPgykf+BTKJtAfvbNNJF3FtLPpJmX883S/tPDXr7M7p41Cc6R8kMHip96EHf5TzSs1Oik4PFiVNNlAa4o0dUD2myEQEM4/1EIbsZO7zmIg1O9aFeu3apYSkmTHCZ6YQOjF48j9pKonJyJugXVeZoTV6egYxu58re+0wQIVvi4Nu/jMmZ45OjZMqwm6jBqQ65bQxmVvIsYherJdP7~-1~-1~-1; _dd_s=rum=2&id=b1a31c04-d995-4502-b194-5242d3295f24&created=1672638157060&expire=1672639158030&logs=0; akavpau_ProdTB=1672638858~id=609763719fdb8936c58eb3434d79a4a1; _ga=GA1.2.31863259.1672632813; AWSALB=+sFh3iWeO2SQUyDhv90JS0AIXF7NEHA21Wz+8Au4iQVSnRS8AoZgPq7OoGyDlnG7GLnFwMbK3wlslLC2acLstSIAotPuUSgIZY/ssbXSmyMieJNf7FzBlY927q96; AWSALBCORS=+sFh3iWeO2SQUyDhv90JS0AIXF7NEHA21Wz+8Au4iQVSnRS8AoZgPq7OoGyDlnG7GLnFwMbK3wlslLC2acLstSIAotPuUSgIZY/ssbXSmyMieJNf7FzBlY927q96; query=039846; _dc_gtm_UA-28553997-18=1; bm_sv=2F9185FDDBF110CD59FEA2E6699E1755~YAAQlaXcFzDAKhmFAQAA2FwCcRLuYnUrUnwF6qWfUaJrbZO6XwvFmNc7xfZLCJgkO1GB20Yap6nf+zmih8X5LdCMabmw7lEdEHZzXu2bbpLaj6g6ZD3CGUCg0ZTl7dCS0DAkuYoTUpClCP4qjcfOSYaHBPp/KgORvzvI9fwlv7tb8OFn42rf2oXx1k+dpakLn6qvjyhPAZo3bQFuamqca/3e7Y7US5EC4VJC9xRlfB09AddR8WrHa2Zd4IJ2x3DFGwQw~1; AMP_7601ffc7c9=JTdCJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJkZXZpY2VJZCUyMiUzQSUyMjdmZTAzNmU4LWI1ZDktNGFmNS1iMGIwLTgyMDYzYmY1YmEyOSUyMiUyQyUyMmxhc3RFdmVudFRpbWUlMjIlM0ExNjcyNjM4MjU4NTYzJTJDJTIyc2Vzc2lvbklkJTIyJTNBMTY3MjYzNTQ4NzI1MCU3RA==; _abck=C2FB400344A2CAAEC831E10FA4A42D02~-1~YAAQhaXcFwX7m2+FAQAAMrQEcQlT4iu8SVll3vH3Q1XI+j4p77DgsPFRXg1A4CIfsLxfjwR9LqI2mPDYRRO6gFe0fpRUuI7Orin7v7ukgQeQ24YnI/8hN/sbSE4ZGlYJg1YBfRXQlQNIvXxc7s5+rS+hz+CZpYiYy20SzwYwLhzMCDEK+VIGPKZ3F3gU5geSu8R2SosdfMmDPLAsx6HKDYZ1Tp67B2QIDWkmJYa6DGPK6/FmbKJLBrOXOk0tgmk+3H6YAe5gqCKdvK2h9F33qx8IyTbrX36DVN60yFUmzAczw4ZNLjWdTruSKlPVm9aC7njERDN3b1vC9Gve8NzOpCgr5gYUFF9wpNs6Wtk3iIsPT5KqXBcuLmAEYkr/6Nagf12+iVPlJu1IIjKxJ/l0awQnx8k088l/1/opYTLshzky+biFOAYw~0~-1~-1; ak_bmsc=B17BDB08E8E13F99F30E725556CE8BBB~000000000000000000000000000000~YAAQlaXcF1ZPJxmFAQAADlXDcBJ/FSra//e4I/YgbxsaKbk1c7sgwN2BxdJIVQJOnh8VNnOfd5efNDLodLrDMIQspIiNguXRLoLDRcjqttPFCxwnPOHUIujQ7QhHjHsozPgfzWbE9h/c5QdHAJHhN5gmi8k9V1c6hpHkIROnn3MiDme7gYi2CIaI3kRaePEFRiK1ZqaxXZBi4JsebVhqF3SaBWexHSkyZEJyab/YjjnUAJhFCgyel6AEOPTpM5OMafdVrlB9qtH+81xs1IxS/dAFD2HLD6oSmUF/i9J+1xGYcwYebxhUoweS2prmlRjmyv2G4C9ijT7R+T1GNBOQTDMlxtJ7Xi1y223jln2XEzPFahXmgWmDVpVWussfWNqicOHZnhAU/tb4zrynxPo=; bm_sv=2F9185FDDBF110CD59FEA2E6699E1755~YAAQhaXcFwb7m2+FAQAAMrQEcRKj3sr1vr6jngIn1buIoybF6ISPqWA1xnE4hfOdzIL9gFAob4pUMKiZ9AEbv+R8o3HW3N9nBsvEZmnhd9qWiaTAiSY04C0y0TttmdMYa7j0Tyd01PCuWSkxE1QDLv7R6kCbLacKCq0Ew6iDuYuQ2n9xnEbM8FC6jVOsVZFGDNzELfW+2sBi3vwR93BL7LEF9Lpa+CTRwoOUeVsSlDXucuhvEEvcxbETac2g0KSuHk0M~1; bm_sz=9614F163ECD1549017422612D9A1368D~YAAQh6XcFy/tvAuFAQAAGiiwcBJt1owPmdpXr9cbbB8n0S6SNw8HCX6eMxGjzIRaTm8darpJIL75PsC4SDWk5XNs2p4EZ4V36rA3DPrA6f6H+kI09Df4Sy7iyCXbaA5TwLwBDeCVjQC7ao+GylppzdC6ve4yONBZrIjSBpyPw4XpEUmN0TzzcVzyDZzhIIknixz2Ybwlc7ApJXzqq743TLIS0FUI+SU5csGMN/SXT/Q3zlfMv8EqW8XVjASY5PLwyOAWMK608jz84rSzDhRcjDzk5ofaR/PPr8WILRM2jvlm0ipOQg==~4469057~3682370; AWSALB=Psv5qm2DfmvJwLnrfXZ1o4kT/Actc1XFTDyvYo43XuBSsfcbzoi6ZWopdjvGQQuEI+jOP7Vuk1zt8tAd0O5MetopD62j9lpi+l/mjoBodA8wz+jBRaMGQ2fDjDWV; AWSALBCORS=Psv5qm2DfmvJwLnrfXZ1o4kT/Actc1XFTDyvYo43XuBSsfcbzoi6ZWopdjvGQQuEI+jOP7Vuk1zt8tAd0O5MetopD62j9lpi+l/mjoBodA8wz+jBRaMGQ2fDjDWV; AWSELB=3119AFC114622B4A1B853AE9C5E9EE3FDC77CA92FEE3DF3643580F87096AEFC09554F284BA063CAD7A343484FD805257476DC3A0ABE21A6E994F0A54FC8B862938F098BD19; AWSELBCORS=3119AFC114622B4A1B853AE9C5E9EE3FDC77CA92FEE3DF3643580F87096AEFC09554F284BA063CAD7A343484FD805257476DC3A0ABE21A6E994F0A54FC8B862938F098BD19; akavpau_ProdTB=1672639011~id=3f9ac111ea73cd9d3ecda2ae7875f489',
        'referer': f'https://www.tacobell.com/food?store={self.store_num}',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-datadog-origin': 'rum',
        'x-datadog-parent-id': '3692794079064169287',
        'x-datadog-sampled': '1',
        'x-datadog-sampling-priority': '1',
        'x-datadog-trace-id': '6488189022316091537'
        }

        await self.get_page(f'https://www.tacobell.com/tacobellwebservices/v2/tacobell/stores/{self.store_num}')
        response = await self.get_page(url)
        #response = await self.fetch(url, headers=headers, payload=payload)
        for category in response['menuProductCategories']:
            for index in category['products']:
                if index['name'] in self.availProducts.keys():
                    if index['name'] == 'Pepsi®':
                        self.menu[f'Small {self.availProducts[index["name"]]}'] = index['variantOptions'][0]['priceData']['value']
                        self.menu[f'Medium {self.availProducts[index["name"]]}'] = index['variantOptions'][1]['priceData']['value']
                        self.menu[f'Large {self.availProducts[index["name"]]}'] = index['variantOptions'][2]['priceData']['value']
                    else:
                        self.menu[self.availProducts[index['name']]] = index['price']['value']



    async def get_store(self, index=0):
        url = f"https://www.tacobell.com/tacobellwebservices/v2/tacobell/stores?latitude={self.address.lat}&longitude={self.address.long}&_=1672632845434"

        payload={}
        headers = {
        'authority': 'www.tacobell.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.tacobell.com/locations',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-datadog-origin': 'rum',
        'x-datadog-parent-id': '5761977405439368353',
        'x-datadog-sampled': '1',
        'x-datadog-sampling-priority': '1',
        'x-datadog-trace-id': '3490034440282567967',
        'Cookie': '_abck=C2FB400344A2CAAEC831E10FA4A42D02~-1~YAAQlaXcF8AbLBmFAQAA6aQacQm4Y+0UzPsX2B5bm7XePnUBzR9NO5g9+tuE8AWT/Nt+kgF6nrKUe90J8DUQx50LidJOljCX35qbQHyWumUrJfmXVhm272IJcDsbCqOSj+J5o391GxWlYDXEQSOPFVfdvheo0g8ugT6jiAWUC5+7baQ2sASm1lEpHEkCPRQuQrLOIpS46DYg1QhcddZ4HHqPzp6EffQ8QG7thHJ2KVBDcJaQ69h9ygghuIVuG2peLQmUt2gCUFjwbOUAEO5HsSjFDbJrA4OSkpG+l8B8Yl0TZLRrt3ztDZMHdExu+worhGyKberX88+puZ5iv+Onae7cHWOS4SM0uNEn56U71JZz2n1CBHf6B56tFJBJ4BiKoe2nrJUJvbbZP8432RKipEmbSdQHdNipSCRqCHEZEj3i1kU+DldA~0~-1~-1; ak_bmsc=4D78054445CB03493F4A241186913FA9~000000000000000000000000000000~YAAQl6XcF3NhVA6FAQAAwmQ2cRIQpP/93xrjDuFGE7wQSRm5Ol/uBTYctWeSp0ttZuv2LHoYx6fUTJBPX0y3d8wv+ShYk739Jdl248gv3jOLs5gqWqC4tZQhchvYn7wp2IRKeXX1P0Kvn17Dw4vqQCsT7PhtX7Y2Wx/wybhyaZtOCHrxzRiypj9N3p1T8P5y/8NCCjPHNtvDe488V+ul3Z29tELdkd0thEdZ9BQCcsHNzUe0g8KI3M81OrzaiCgrgM+/svdQIgoIEgVkjSUtfI5oKIzSnLFfXpoArjnE58+arqoFLPZbMyBY1K6Zq2IcU7t2xy8z1zfPz4w4g4yqATFXXvXjtyBPhV7dFJEV1guWxLmySsL7SirM1p+v5YKCZl7sRm/Zw4H3b4WPRBo=; bm_sv=066C9A8217D8C309227945471237700A~YAAQl6XcF3YcVQ6FAQAAJ509cRLWHY5nAnA8xXkxMKU868KCRzxgZSYuSDYYKaMRCW7bNDHYqWRjtcvW7IZx1CHuROCwDXiCB0G8vQGmg/1IkAtzvwK3ZjQRT/MuuHf6nYHx9eUEfG4LYAwjx6znUXhYiBAoWK+ZoYFP228zHfDdpg6efCrGCweXV5ExEUb53T4RxSn+WOkUOooctqSgferpvP3G9/PWfhYzwrArD/hn6EfNcFDjKjTvuafyLDkSt68=~1; bm_sz=9614F163ECD1549017422612D9A1368D~YAAQh6XcFy/tvAuFAQAAGiiwcBJt1owPmdpXr9cbbB8n0S6SNw8HCX6eMxGjzIRaTm8darpJIL75PsC4SDWk5XNs2p4EZ4V36rA3DPrA6f6H+kI09Df4Sy7iyCXbaA5TwLwBDeCVjQC7ao+GylppzdC6ve4yONBZrIjSBpyPw4XpEUmN0TzzcVzyDZzhIIknixz2Ybwlc7ApJXzqq743TLIS0FUI+SU5csGMN/SXT/Q3zlfMv8EqW8XVjASY5PLwyOAWMK608jz84rSzDhRcjDzk5ofaR/PPr8WILRM2jvlm0ipOQg==~4469057~3682370; AWSALB=kKN+PoM7B//HDuLWHZD1dylPay+j28JBqc2SP246SwhrIlF6fG1pT/KGVimXPK5u5/e5IKb8zE9txZTfFOuCeqlQ94J2bzQ8pOqq0Nm5xbqKNwi5AGtEzRTaNU+A; AWSALBCORS=kKN+PoM7B//HDuLWHZD1dylPay+j28JBqc2SP246SwhrIlF6fG1pT/KGVimXPK5u5/e5IKb8zE9txZTfFOuCeqlQ94J2bzQ8pOqq0Nm5xbqKNwi5AGtEzRTaNU+A; AWSELB=3119AFC114622B4A1B853AE9C5E9EE3FDC77CA92FEE3DF3643580F87096AEFC09554F284BA063CAD7A343484FD805257476DC3A0ABE21A6E994F0A54FC8B862938F098BD19; AWSELBCORS=3119AFC114622B4A1B853AE9C5E9EE3FDC77CA92FEE3DF3643580F87096AEFC09554F284BA063CAD7A343484FD805257476DC3A0ABE21A6E994F0A54FC8B862938F098BD19; akavpau_ProdTB=1672642741~id=39173ad185e6c8052650343b83d163d3'
        }



        response = await self.get_page(url)
        nearby = "nearByStores"
        online = "currentOnlineAvailable"
        if 'storefindersearchpage' in response.keys():
            response = response['storefindersearchpage']
            nearby = "nearbystores"
            online = online.lower()
        try:
            if response[nearby][index][online] == False or response[nearby][index][online] == 'false':
                self.store_index+=1
                await self.get_store(self.store_index)
                await self.scrape_menu()
                return
            self.store_num = response[nearby][index]['name']
            self.address.address = response[nearby][index]['address']['line1']
        except IndexError:
            self.store_num = None
        except KeyError:
            self.store_num = None