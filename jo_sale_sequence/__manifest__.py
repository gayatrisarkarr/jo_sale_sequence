{
    'name': 'JO Sale Sequence',
    'version': '19.0.1.0.0',
    'summary': 'Custom Sale Order sequence: JIPL/SO/Ref/MonthYear/XXXX',
    'category': 'Sales',
    'depends': ['sale', 'product', 'purchase', 'account', 'stock', 'project', 'sale_project'],
    'data': [
        'views/hsn_views.xml',
        'views/partner_gst_treatment_views.xml',
        'views/purchase_views.xml',
        'views/sale_order_approval_views.xml',
        'views/sale_order_checklist_views.xml',
        'views/project_extension_views.xml',
        'views/product_url_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
