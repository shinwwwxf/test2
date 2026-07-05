#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
        
        # 👇 修改這段：同時繞過版本檢查與 RETURNING 新語法
        from django.db.backends.base.base import BaseDatabaseWrapper
        from django.db.backends.mysql.features import DatabaseFeatures
        
        # 1. 繞過版本檢查
        BaseDatabaseWrapper.check_database_version_supported = lambda self: None
        
        # 2. 強制告訴 Django：這個資料庫「不支援」RETURNING 語法
        DatabaseFeatures.can_return_rows_from_insert = property(lambda self: False)
        DatabaseFeatures.can_return_columns_from_insert = property(lambda self: False)
        
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    
if __name__ == '__main__':
    main()
