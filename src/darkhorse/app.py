"""
Super lightweight and simple Cardano wallet
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from pycardano import ExtendedSigningKey, ExtendedVerificationKey, Address, Network, HDWallet
import json

cardano_account_info = []

class DarkHorse(toga.App):

    def create_hd_wallet(self, button):
        network = Network.TESTNET
        if self.mnemonic_input.value:
            mnemonic_phrase = self.mnemonic_input.value
        else:
            mnemonic_phrase = HDWallet.generate_mnemonic()
        wallet = HDWallet.from_mnemonic(mnemonic_phrase)      
        payment_signing_key = ExtendedSigningKey.from_hdwallet(wallet)
        payment_verification_key = ExtendedVerificationKey.from_signing_key(payment_signing_key)
        address = Address(payment_part=payment_verification_key.hash(), network=network)

        to_json_payment_signing_key = json.loads(str(payment_signing_key))
        to_json_payment_verification_key = json.loads(str(payment_verification_key))

        self.mnemonic_text.value = mnemonic_phrase
        self.payment_key.value = to_json_payment_signing_key['cborHex']
        self.verification_key.value = to_json_payment_verification_key['cborHex']
        self.public_address.value = address 

        cardano_account_info.append(self.public_address.value)
        cardano_account_info.append(self.payment_key.value)
        cardano_account_info.append(self.verification_key.value)
        cardano_account_info.append(self.mnemonic_text.value)

    def show_second_window(self, widget):
        
        account_label = toga.Label('Account Dashboard')
        account_label.style.padding = 10
        public_address_text = toga.TextInput()
        public_address_text.style.padding = 10
        public_address_text.value = cardano_account_info[0]
        account_mnemonic_text = toga.TextInput()
        account_mnemonic_text.style.padding = 10
        account_mnemonic_text.value = cardano_account_info[1]
        account_payment_key = toga.TextInput()
        account_payment_key.style.padding = 10
        account_payment_key.value = cardano_account_info[2]
        account_verification_key = toga.TextInput()
        account_verification_key.style.padding = 10
        account_verification_key.value = cardano_account_info[3]

        second_box = toga.Box(style=Pack(direction=COLUMN, padding=10), children=[account_label, public_address_text, account_mnemonic_text, account_payment_key, account_verification_key])
        self.main_window.content = second_box
        self.main_window.show()

    def show_create_window(self, widget):
        pass
        
    def startup(self):
        
        
        account_icon = "resources/account"
        create_icon = "resources/create"

        navbar = toga.Group("Navbar")
        account_dashboard_cmd = toga.Command(
            self.show_second_window,
            text="Account dashboard",
            tooltip="Go to account dashboard",
            icon=account_icon,
            group=navbar,
        )
        create_account_cmd = toga.Command(
            self.show_create_window,
            text="Create account",
            tooltip="Create another account",
            icon=create_icon,
            group=navbar,
        )
        

        # Draw import from mnemonic interface
        mnemonic_label = toga.Label('Import from mnemonic')
        mnemonic_label.style.padding = 10
        self.mnemonic_input = toga.PasswordInput()
        self.mnemonic_input.style.padding = 10
        import_button = toga.Button("Import", on_press=self.create_hd_wallet)
        import_button.style.padding = 10

        # Draw create fresh account interface
        create_account_label = toga.Label('Create fresh account')
        create_account_label.style.padding = 10
        create_button = toga.Button("Create", on_press=self.create_hd_wallet)
        create_button.style.padding = 10
        self.public_address = toga.TextInput()
        self.public_address.style.padding = 10
        self.payment_key = toga.TextInput()
        self.payment_key.style.padding = 10
        self.verification_key = toga.TextInput()
        self.verification_key.style.padding = 10
        self.mnemonic_text = toga.TextInput()
        self.mnemonic_text.style.padding = 10

        create_from_mnemonic_box = toga.Box(style=Pack(direction=COLUMN, padding=10), children=[mnemonic_label, self.mnemonic_input, import_button])
        create_fresh_account_box = toga.Box(style=Pack(direction=COLUMN, padding=10), children=[create_account_label, create_button, self.public_address, self.mnemonic_text, self.payment_key, self.verification_key])                                    
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10), children=[create_from_mnemonic_box, create_fresh_account_box])

        self.commands.add(account_dashboard_cmd)
        self.commands.add(create_account_cmd)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.toolbar.add(account_dashboard_cmd)
        self.main_window.toolbar.add(create_account_cmd)
        self.main_window.content = main_box
        self.main_window.show()

def main():
    return DarkHorse()
