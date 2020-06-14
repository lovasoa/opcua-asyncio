from textwrap import dedent
from generate_statuscode import status_codes
from string import Template
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    codes = status_codes()

    with open(os.path.join(BASE_DIR, "asyncua", "ua", "uaerrors", "_auto.py"), "w") as f:
        preamble = """\
        #AUTOGENERATED!!!

        from asyncua.ua.uaerrors import UaStatusCodeError


        """

        f.write(dedent(preamble))

        for name, code, _ in codes:
            # skip non-bad because they should not be thrown as exceptions
            if not name.startswith("Bad"):
                continue

            template = Template(dedent("""\
            class $name(UaStatusCodeError):
                code = $code
            """))
            print(template.safe_substitute(name=name, code=code), file=f)
