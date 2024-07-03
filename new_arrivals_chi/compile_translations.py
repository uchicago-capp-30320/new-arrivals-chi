import os
import subprocess

def compile_translations():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    translations_dir = os.path.join(script_dir, 'translations')
    if not os.path.exists(translations_dir):
        print(f"Error: {translations_dir} directory does not exist.")
        return
    
    for locale in os.listdir(translations_dir):
        locale_dir = os.path.join(translations_dir, locale, 'LC_MESSAGES')
        po_file = os.path.join(locale_dir, 'messages.po')
        mo_file = os.path.join(locale_dir, 'messages.mo')
        if os.path.exists(po_file):
            print(f"Compiling {po_file} to {mo_file}")
            result = subprocess.run(['msgfmt', '-o', mo_file, po_file], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"Error compiling {po_file}: {result.stderr}")
            else:
                print(f"Successfully compiled {po_file} to {mo_file}")
        else:
            print(f"PO file not found: {po_file}")

if __name__ == "__main__":
    compile_translations()
