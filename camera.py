from flet import *
import cv2
import time
import os

def main(page: Page):
    page.update()

    camera_info = {
        'ip': '10.0.10.11',
        'name': 'Floreça',
        'channels': ["3"],
        'USERNAME': 'admin',
        'PASSWORD': '102030Aa'
    }

    def generate_rtsp_url(camera_info):
        ip = camera_info['ip']
        username = camera_info['USERNAME']
        password = camera_info['PASSWORD']
        channel = camera_info['channels'][0]  # Usa o primeiro canal da lista
        return f"rtsp://{username}:{password}@{ip}:554/cam/realmonitor?channel={channel}&subtype=0"

    minhaimagem = Image(
        src=False,
        width=300,
        height=300,
        fit="cover"
    )

    rtsp_url = generate_rtsp_url(camera_info)

    def Capture(e):
        cap = cv2.VideoCapture(rtsp_url)
        cv2.namedWindow("Paroquia", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Paroquia", 400, 600)

        timestamp = str(int(time.time()))
        meuarquivoface = str("meuarquivoface" + "_" + timestamp + '.jpg')
        try:
            while True:
                ret, frame = cap.read()
                cv2.imshow("Paroquia", frame)
                minhaimagem.src = ""
                page.update()

                key = cv2.waitKey(1)

                if key == ord("q"):
                    break
                elif key == ord("s"):
                    cv2.imwrite(f"foto/{meuarquivoface}", frame)
                    cv2.putText(frame, "Salvo com sucesso !!!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow("Paroquia", frame)
                    cv2.waitKey(3000)
                    folder_path = "foto/"
                    minhaimagem.src = folder_path + meuarquivoface
                    page.update()
                    break

            cap.release()
            cv2.destroyAllWindows()
            page.update()

        except Exception as e:
            print(e)
            print("deu erro")

    page.add(
        Column([
            Text("Capture a Imagem",
                 size=30, weight="bold"
                 ),
            ElevatedButton("Capture minha Face",
                           bgcolor="blue", color="white",
                           on_click=Capture
                           ),
            minhaimagem
        ])
    )

app(target=main, assets_dir="foto")