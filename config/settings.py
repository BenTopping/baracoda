def development_config():
    return { 
        'prefixes': [
            {
                'prefix': 'SANG',
                'description': 'Sanger barcodes'
            },
            {
                'prefix': 'NIRE',
                'description': 'Nire barcodes'
            }
        ],
        'valid_prefixes': ['SANG', 'NIRE'],
        'sequence_name': 'heron',
        'sequence_start': 1
    }

def testing_config():
    return { 
        'prefixes': [
            {
                'prefix': 'SANG',
                'description': 'Sanger barcodes'
            },
            {
                'prefix': 'NIRE',
                'description': 'Nire barcodes'
            }
        ],
        'valid_prefixes': ['SANG', 'NIRE'],
        'sequence_name': 'heron',
        'sequence_start': 1,
        'reset_sequence': True
    }

def production_config():
    return development_config()
