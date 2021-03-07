# Copyright 2019 ForgeFlow, S.L.
# Copyright 2020 CorporateHub (https://corporatehub.eu)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountBankStatementImportSheetMapping(models.Model):
    _name = 'account.bank.statement.import.sheet.mapping'
    _description = 'Account Bank Statement Import Sheet Mapping'

    name = fields.Char(
        required=True,
    )
    float_thousands_sep = fields.Selection(
        string='Thousands Separator',
        selection=[
            ('dot', 'dot (.)'),
            ('comma', 'comma (,)'),
            ('none', 'none'),
        ],
        default='dot',
    )
    float_decimal_sep = fields.Selection(
        string='Decimals Separator',
        selection=[
            ('dot', 'dot (.)'),
            ('comma', 'comma (,)'),
            ('none', 'none'),
        ],
        default='comma',
    )
    file_encoding = fields.Selection(
        string='Encoding',
        selection=[
            ('utf-8', 'UTF-8'),
            ('utf-8-sig', 'UTF-8 (with BOM)'),
            ('utf-16', 'UTF-16'),
            ('utf-16-sig', 'UTF-16 (with BOM)'),
            ('windows-1252', 'Western (Windows-1252)'),
            ('iso-8859-1', 'Western (Latin-1 / ISO 8859-1)'),
            ('iso-8859-2', 'Central European (Latin-2 / ISO 8859-2)'),
            ('iso-8859-4', 'Baltic (Latin-4 / ISO 8859-4)'),
            ('big5', 'Traditional Chinese (big5)'),
            ('gb18030', 'Unified Chinese (gb18030)'),
            ('shift_jis', 'Japanese (Shift JIS)'),
            ('windows-1251', 'Cyrillic (Windows-1251)'),
            ('koi8_r', 'Cyrillic (KOI8-R)'),
            ('koi8_u', 'Cyrillic (KOI8-U)'),
        ],
        default='utf-8',
    )
    skip_lines_start = fields.Integer(
        string='Skip prefix lines',
        help=(
            'If the csv file has a heading area upfront the lines representing the table with the actual '
            'bank statement lines, enter the number of lines to skip at the beginning of the file here. '
            'The parser will ignore this amount of lines at the beginning of the file when trying to parse.'
        ),
    )
    skip_lines_end = fields.Integer(
        string='Skip suffix lines',
        help=(
            'If the csv file has a suffix area below the lines representing the table with the actual '
            'bank statement lines, enter the number of lines to skip at the end of the file here. '
            'The parser will ignore this amount of lines at the end of the file when trying to parse.'
        ),
    )
    delimiter = fields.Selection(
        string='Delimiter',
        selection=[
            ('dot', 'dot (.)'),
            ('comma', 'comma (,)'),
            ('semicolon', 'semicolon (;)'),
            ('tab', 'tab'),
            ('space', 'space'),
            ('n/a', 'N/A'),
        ],
        default='comma',
    )
    header_relabel = fields.Char(
        string='Relabel columns',
        help=(
            'Relabel columns when the csv file has columns with missing labels which cannot be mapped to '
            'their column counter parts in the mapping. Use the number of the column and the desired label '
            'For example "0:Timestamp,12:DebitCredit". Use the customized labels in the columns section to '
            'include the customized columns in the parsing process.'
        ),
    )
    quotechar = fields.Char(
        string='Text qualifier',
        size=1,
        default='"',
    )
    timestamp_format = fields.Char(
        string='Timestamp Format',
        required=True,
    )
    timestamp_column = fields.Char(
        string='Timestamp column',
        required=True,
    )
    currency_column = fields.Char(
        string='Currency column',
        help=(
            'In case statement is multi-currency, column to get currency of '
            'transaction from'
        ),
    )
    amount_column = fields.Char(
        string='Amount column',
        required=True,
        help='Amount of transaction in journal\'s currency',
    )
    balance_column = fields.Char(
        string='Balance column',
        help='Balance after transaction in journal\'s currency',
    )
    original_currency_column = fields.Char(
        string='Original currency column',
        help=(
            'In case statement provides original currency for transactions '
            'with automatic currency conversion, column to get original '
            'currency of transaction from'
        ),
    )
    original_amount_column = fields.Char(
        string='Original amount column',
        help=(
            'In case statement provides original currency for transactions '
            'with automatic currency conversion, column to get original '
            'transaction amount in original transaction currency from'
        ),
    )
    debit_credit_column = fields.Char(
        string='Debit/credit column',
        help=(
            'Some statement formats use absolute amount value and indicate sign'
            'of the transaction by specifying if it was a debit or a credit one'
        ),
    )
    debit_value = fields.Char(
        string='Debit value',
        help='Value of debit/credit column that indicates if it\'s a debit',
        default='D',
    )
    credit_value = fields.Char(
        string='Credit value',
        help='Value of debit/credit column that indicates if it\'s a credit',
        default='C',
    )
    transaction_id_column = fields.Char(
        string='Unique transaction ID column',
    )
    description_column = fields.Char(
        string='Description column',
    )
    merge_description_keep_newlines = fields.Integer(
        string='Merge description lines',
        help=('In csv files where the description column contains line breaks, this field can be used '
              'to deal with them. Left blank no merging of line breaks will happen. Set to 0 all line breaks '
              'will be removed. Any number stands for the amount of line breaks which will be kept '
              'counting from the beginning e.g. 1 will erase all line breaks after the first one.'
        ),
    )

    notes_column = fields.Char(
        string='Notes column',
    )
    reference_column = fields.Char(
        string='Reference column',
    )
    partner_name_column = fields.Char(
        string='Partner Name column',
    )
    bank_name_column = fields.Char(
        string='Bank Name column',
        help='Partner\'s bank',
    )
    bank_account_column = fields.Char(
        string='Bank Account column',
        help='Partner\'s bank account',
    )
    bank_account_iban_from_description = fields.Boolean(
        string='Parse IBAN from description',
        help='In cases where the bank csv file contains the IBAN Account numbers from counterparts in '
             'the description column, you can check this box and the number will be parsed from the '
             'description and filled in the bank account column in the bank statement line.',
    )

    @api.onchange('float_thousands_sep')
    def onchange_thousands_separator(self):
        if 'dot' == self.float_thousands_sep == self.float_decimal_sep:
            self.float_decimal_sep = 'comma'
        elif 'comma' == self.float_thousands_sep == self.float_decimal_sep:
            self.float_decimal_sep = 'dot'

    @api.onchange('float_decimal_sep')
    def onchange_decimal_separator(self):
        if 'dot' == self.float_thousands_sep == self.float_decimal_sep:
            self.float_thousands_sep = 'comma'
        elif 'comma' == self.float_thousands_sep == self.float_decimal_sep:
            self.float_thousands_sep = 'dot'

    @api.multi
    def _get_float_separators(self):
        self.ensure_one()
        separators = {
            'dot': '.',
            'comma': ',',
            'none': '',
        }
        return (separators[self.float_thousands_sep],
                separators[self.float_decimal_sep])

    @api.model
    def _decode_column_delimiter_character(self, delimiter):
        return ({
            'dot': '.',
            'comma': ',',
            'semicolon': ';',
            'tab': '\t',
            'space': ' ',
        }).get(delimiter)

    @api.multi
    def _get_column_delimiter_character(self):
        return self._decode_column_delimiter_character(self.delimiter)
