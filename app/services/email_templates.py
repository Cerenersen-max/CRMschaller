"""Not: 'Outlook/Partnership ... lifestyle collaboration - Mime-Version:(1.0)
content-Type: text/plain; charset=utf-8; content-Transfer-encoding: quoted
printable' - Aston Martin (Toronto Operations) ile ortaklik yazismasinda
kullanilan basliklarin karsiligi. Yatirimci/partner iletisimi icin (ornegin
lojistik dosyasindaki 'bankalara mail iletildi' adimi ya da yeni bir partner
ile ilk temas icin) standart bir MIME e-posta uretir."""
from __future__ import annotations

from email.message import EmailMessage


def build_partnership_email(
    to_name: str,
    to_email: str,
    subject: str,
    body_text: str,
    from_address: str = "partnerships@cenora.com",
) -> EmailMessage:
    """Notlardaki Outlook basliklarina (Mime-Version, charset=utf-8,
    quoted-printable) uygun bir metin e-postasi olusturur. SMTP gonderimi bu
    fonksiyonun disinda, cagiran taraf tarafindan yapilir."""
    message = EmailMessage()
    message["From"] = from_address
    message["To"] = f"{to_name} <{to_email}>"
    message["Subject"] = subject
    message["MIME-Version"] = "1.0"
    # set_content varsayilan olarak quoted-printable + utf-8 kullanir (notlardaki
    # 'content-Transfer-encoding: quoted printable, charset=utf-8' ile birebir eslesir).
    message.set_content(body_text, charset="utf-8")
    return message


def build_aston_martin_partnership_email(to_name: str, to_email: str) -> EmailMessage:
    """Not: 'Partner (Toronto Operations) x Aston Martin' - lifestyle
    collaboration ilk temas e-postasi. Gizlilik nedeniyle gercek kisi
    adi/e-postasi kod icinde tutulmaz; ilgili Investor kaydindan (bkz.
    GET /investors/{id}/outreach-email-preview) cagiran taraf tarafindan
    saglanir."""
    return build_partnership_email(
        to_name=to_name,
        to_email=to_email,
        subject="Cenora x Aston Martin - Lifestyle Collaboration",
        body_text=(
            f"Merhaba {to_name},\n\n"
            "Cenora olarak Aston Martin ile bir lifestyle collaboration "
            "firsatini degerlendirmek isteriz. Uygun oldugunuz bir tarihte "
            "gorusme ayarlayabilir miyiz?\n\nSaygilarimizla,\nCenora Partnerships"
        ),
    )
