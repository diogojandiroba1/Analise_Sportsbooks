import requests
import json
from time import sleep





while True:

    #BETPIX365

    url = "https://f12.bet.br/modules/sports/ajax.php"
    
    headers = {
    ':authority': 'f12.bet.br',
    ':method': 'GET',
    ':path': '/modules/sports/ajax.php?action=get_odds&json=1&carousel=1&lid=65096&append=1&',
    ':scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
    'cookie': '_cs_c=1; _cs_cvars=%7B%7D; _tgpc=9a866253-0d81-529e-a798-19c8f3bb0629; AdoptVisitorId=CYVmCYAYDMFMEYC0x4GMCciAs0BGvF0QBDJVVLAdgA55wA2Y1ayoA===; BIAB_LANGUAGE=PT_BR; BIAB_TZ=180; twk_uuid_665a05729a809f19fb3766db=%7B%22uuid%22%3A%221.MSKoRORtAjhLFWS1wnT8gD78A6rJptyURl2MundwjvPYGvDFbptvu3jDADQXVoN6L3eZgaozhrYtLmpF9OQHtkV7g9yfULoQl6ooJlBZdYU2Z%22%2C%22version%22%3A3%2C%22domain%22%3A%22bet.br%22%2C%22ts%22%3A1739376526803%7D; fs_uid=#o-6N9J-eu1#0ddfd012-7ff6-4eda-abec-6bb4c465d571:4ffced8c-6bb5-4188-b24c-8aa37514eab1:1739400924462::1#/1770393398; lo-uid=d9690c96-1740063514451-24f63c0a4f923a33; lo-visits=1; _cs_id=e5322a77-b226-a0fb-8483-a1fd7c2791a8.1737084249.7.1740063756.1740063714.1684334019.1771248249126; AdoptConsent=N4Ig7gpgRgzglgFwgSQCIgFwgAwA4DMATLgGwCGAjALT4CsAnACxWMBm9AxlVGbcxVADsAE0KF6+KPWGsQAGhAA3OPAQB7AE7JhmEMNqjsrCNWEUO9FqyhQq9WpSocOjQbgqFyHXIPkg1AA4IyAB2ACpkAOYwmADaIPgAVgCOABIAigghahAANn4QZACugqwOALLljH4AykWM6QAagjXIJIl+UKgAYgCCYADWuWQAFiR+HFABADIUALbCA2pUfgiRNbnCAOqJhMgAQn5qCNgDAKoACgCaRWEAXn4A0rTT9eLIUAh+APIAwrkATzYZEU2A0BVSAA9FAA1CAaRqPcp+O5bb4kABK+yg+woNT85WQRUIGmEAHEihs/Pt6LkthwRls7gFfn5kAA5BBXGFzMkwKgUEAAXQUgQQ3yKCAi0TiIpAHDUIRgEBCwR0WFSAH0QiF8GACooVVKAQEILoEBjHukRFaJorlaq4Rp4IrMNgFEUAsIyEhhL0vlhCNhCLQqMGqGIwsGMGIMHwAHT4CgkABaIAAvkA===; datadome=6HRwfYLyZgiQWj4lVDChcoHzQM~dVE_P~zZAcN3OdY_ISQquE5Sop8IX0er_PW6T2490dSDza362~I~hyhS5CUTTCTqRCYQyfBpGyBNcrqwKRt_G9mg7fn70cMswRV7U; twk_uuid_677c4b07af5bfec1dbe77ad9=%7B%22uuid%22%3A%221.MSKuAtJo9lhngIR4avSxA5jd0rjrHeqTMpcc8I6s0WNeE6mLpJqAFiRE2NajetyU6G3sVNoltoLu5jjTR0vwjH6VcJ7PJeqlkIGObR1u9efWV%22%2C%22version%22%3A3%2C%22domain%22%3A%22bet.br%22%2C%22ts%22%3A1740234695288%7D; C_U_I=141570; _tglksd=eyJzIjoiMjEzYmRlYTAtNjliOC01YjA0LThjZmYtYzc2N2FhOTc3YmM4Iiwic3QiOjE3NDAyMzUzMzg5NjEsImciOiJDandLQ0FpQTJKRzlCaEF1RWl3QUhfemYzak5JUkFQeUs2MkVxc2pSdEdYSzJiU1ZBTkFYcjVfR2ZObHJsMjdLaGhuQzdjR0g3TWZKU3hvQzl3Z1FBdkRfQndFIiwiZ3QiOjE3Mzg4NTczODYxMjYsInNvZCI6IihkaXJlY3QpIiwic29kdCI6MTc0MDIzMzA3MDY5OCwic29kcyI6Im8iLCJzb2RzdCI6MTc0MDIzMzA3MDY5OH0=; _sp_srt_id.b907=b38d2406-e041-4664-94e6-bc75a3e7db3f.1737297311.8.1740247388.1740094267.73d005c8-dafb-4c39-ab6a-f4055dd45b59.f57887a4-b5aa-4535-a7fe-7d5ea9285e9a...0; Qualtrics_Cookie=0; _rdt_uuid=1737084400063.92a8f73b-cfa0-4438-8f6c-90a30134d9f7; fanplayr=%7B%22uuid%22%3A%221739888968258-b424ceed16f4e351c75ffffb%22%2C%22uk%22%3A%225.nZpaeWLiqw0csICkSBU.1739888979%22%2C%22sk%22%3A%220b26b138acff10c700d042b00f4659f6%22%2C%22se%22%3A%22e1.fanplayr.com%22%2C%22tm%22%3A1%2C%22t%22%3A1740258473306%7D; zpstorage_YzRmZjk2MWItYjMxYS00ZDJlLWFiZTEtOTE3ZWZmMGZhZjRmzibet.br=ImEyOTM0MGFhLTJmNmYtNDMxYy04OTRmLThhOTA4YTFmY2VjZCI%3D; _sp_id.b907=79bedac8-07ed-4edb-88ce-49cfe3181ad3.1740265244.1.1740266050.1740265244.10e87cb8-4351-4b40-827a-515363fe9373; ph_phc_wUcGl0XPucm5gSawpdPMBP8mdQoXUO9HgrvFHndWc8P_posthog=%7B%22distinct_id%22%3A%220194ffe2-63fe-7333-bf4d-cd795bbf7c20%22%2C%22%24sesid%22%3A%5B1740270901406%2C%2201953038-f30d-74ac-b4bf-c0b9bf1e7345%22%2C1740270793485%5D%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22u%22%3A%22https%3A%2F%2Fwww.estrelabet.bet.br%2Fpb%2Fcadastro%3Faffid%3D347128%26campaign_id%3D22953%26utm_source%3Dgoogle%26utm_medium%3Dcpc%26utm_campaign%3Dmarca%26afp%3Dpura%26afp3%3Dad1%26afp2%3Destrela%2520bet%26gad_source%3D1%26gclid%3DCjwKCAiAzba9BhBhEiwA7glbakD64YgFdMP94R8G_YxzzesCPrJ3jXjZD85RfOr8P9BqQDqE4aL2

    }
    
    caminho_arquivo = "data\\dataf12bet.json"


    try:
            response = requests.get(url, headers=headers) 
            response.raise_for_status() 
            
            dados_json = response.json()
            print("Dados obtidos com sucesso!")
            
            with open(caminho_arquivo,'w', encoding='utf-8') as arquivo:
                json.dump(dados_json, arquivo, ensure_ascii=False, indent=4)
                print("dados salvos")
                
    except requests.exceptions.SSLError as e:
            print(f"Erro de SSL/TLS: {e}")
            
    except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            

    sleep(60)
####################################################################################################################################################################################################