# Install first (one-time):
#   pip install graphviz
#   # plus Graphviz binaries: https://graphviz.org/download/

from graphviz import Digraph

dot = Digraph('RosterlyPaymentSync', filename='rosterly_payment_sync', format='png')

# ── External sources ────────────────────────────────
dot.attr('node', shape='rectangle', style='filled', color='lightblue')
dot.node('QBO',   'QuickBooks Online')
dot.node('Plaid', 'Plaid API')

# ── Sync workers ────────────────────────────────────
dot.attr('node', shape='rectangle', style='filled', color='lightgreen')
dot.node('QBOWorker',   'QBO Payment\nSync Worker')
dot.node('PlaidWorker', 'Plaid Payment\nSync Worker')

# ── Core domain models ──────────────────────────────
dot.attr('node', shape='rectangle', style='filled', color='khaki')
dot.node('Payment',        'Payment (root)')
dot.node('QboPayment',     'QboPayment')
dot.node('PlaidPayment',   'PlaidPayment')
dot.node('ManualPayment',  'ManualPayment')
dot.node('PaymentLine',    'PaymentLineItem')
dot.node('Invoice',        'Invoice')
dot.node('CustInv',        'CustomerInvoice')
dot.node('VendInv',        'VendorInvoice')

# ── Services ────────────────────────────────────────
dot.attr('node', shape='rectangle', style='filled', color='orange')
dot.node('Reconcile',  'Reconciliation Service')
dot.node('UpdStatus',  'Invoice Status Updater')

# ── Persistence ─────────────────────────────────────
dot.attr('node', shape='cylinder', style='filled', color='plum')
dot.node('DB', 'Postgres\nRosterly DB')

# ── Data-flow edges (solid) ─────────────────────────
dot.attr('edge', style='solid')
dot.edges([('QBO', 'QBOWorker'), ('QBOWorker', 'Payment'),
           ('Plaid', 'PlaidWorker'), ('PlaidWorker', 'Payment'),
           ('Payment', 'Reconcile'), ('Reconcile', 'PaymentLine'),
           ('PaymentLine', 'Invoice'), ('Invoice', 'UpdStatus')])

# ── Model relationships (dashed) ────────────────────
dot.attr('edge', style='dashed')
dot.edge('Payment', 'QboPayment',     label='1 : 1')
dot.edge('Payment', 'PlaidPayment',   label='1 : 1')
dot.edge('Payment', 'ManualPayment',  label='1 : 1')
dot.edge('Payment', 'PaymentLine',    label='1 : *')
dot.edge('PaymentLine', 'Invoice',    label='* : 1')
dot.edge('Invoice', 'CustInv',        label='is-a')
dot.edge('Invoice', 'VendInv',        label='is-a')

# ── Render to PNG & view ────────────────────────────
dot.render(view=True)      # creates rosterly_payment_sync.png

