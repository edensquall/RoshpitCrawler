from .models import Base, engine
from .models import item, item_type, notify, parameter, property, user, wish, wish_property

# 建立資料庫
Base.metadata.create_all(engine)
