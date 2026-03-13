import base64
import io
import socket

import qrcode


def _obtener_ip_local():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("10.255.255.255", 1))
        return sock.getsockname()[0]
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return "127.0.0.1"
    finally:
        sock.close()


def _generar_qr_base64(url):
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(url)
    qr.make(fit=True)

    imagen = qr.make_image(fill_color="#2c3e50", back_color="white")
    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")


def construir_contexto_acceso_movil(request, path="/admin/"):
    current_host = request.get_host().split(":")[0]
    host = current_host if current_host not in {"127.0.0.1", "localhost", "0.0.0.0"} else _obtener_ip_local()
    port = request.get_port() or "8000"
    scheme = "https" if request.is_secure() else "http"
    url = f"{scheme}://{host}:{port}{path}"

    return {
        "acceso_movil_host": host,
        "acceso_movil_url": url,
        "acceso_movil_qr_base64": _generar_qr_base64(url),
        "acceso_movil_requiere_red_local": host not in {"127.0.0.1", "localhost"},
    }