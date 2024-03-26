import os
def log(info_dict):
    try:
        with open(r'H:\app\bt-video\log.txt','a+') as file:
            for key,value in info_dict.items():
                print(f'{key}:{info_dict[key]}')
                file.writelines(f'{key}:{info_dict[key]}')
            return
    except:
        os.mkdir(r'H:\app\bt-vedio\log.txt')
        log(info_dict)

if __name__=='__main__':
    log_dict={
        "name":'ss'
        ,'url':'url'
    }
    log(log_dict)