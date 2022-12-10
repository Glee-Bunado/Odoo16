{
    'name': 'Real Estate',
    'category': 'Real Estate/Brokerage',
    'depends': [
            'base',
            'web',
            # 'web_dashboard'
           ],
    'data': [
        'views/security.xml',
        'data/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'data/estate.property.type.csv',
        'report/estate_reports.xml',
        'report/estate_report_views.xml',

        ],
    "demo": [
        "demo/property_tag.xml",
        "demo/estate_property.xml",
        "demo/estate_offer.xml",
    ],
    "application": True,
}
