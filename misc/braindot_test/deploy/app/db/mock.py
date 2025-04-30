import sqlalchemy
from .db_session import SqlAlchemyBase

class Mock(SqlAlchemyBase):
    __tablename__ = "mocks"
    
    id:int = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True, autoincrement=True)

    first_name:str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    last_name:str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    info:str = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    score:int = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

default_mocks = [
    Mock(first_name="Bombombini", last_name="Gusini", info="Привет, я Bombombini Gusini! Маленький, но не вздумай недооценивать — я взрываюсь в нужный момент 💥", score=83),
    Mock(first_name="Trippi", last_name="Troppi", info="Я Trippi Troppi! Вечно в движении, вечно в переборе. Один я — как трое!", score=77),
    Mock(first_name="Capuchino", last_name="Assassino", info="Capuchino Assassino к вашим услугам. Я сладкий, крепкий и могу быть смертельно бодрящим ☕💀", score=91),
    Mock(first_name="Frulli", last_name="Frulla", info="Меня зовут Frulli Frulla, и я здесь, чтобы закружить тебя в вихре безумия! Вруум!", score=70),
    Mock(first_name="Bobritto", last_name="bandito", info="Эй, амиго! Я Bobritto bandito — обёрнут, заряжен, и всегда на грани закона 🌯🦹‍♂️", score=85),
    Mock(first_name="Chimpanzini", last_name="Bananini", info="Я Chimpanzini Bananini! Мои бананы — мои братья. Шалю, смеюсь и живу в ритме джунглей!", score=78),
    Mock(first_name="Tung Tung", last_name="Tung Sahur", info="Tung Tung Tung Sahur здесь! Я барабаню на рассвете, и весь мир просыпается под мой бит 🥁🌅", score=74),
    Mock(first_name="Brr brr", last_name="Patapim", info="Я Brr brr Patapim! Двигаюсь быстро, шумлю громко, прихожу неожиданно и оставляю только эхо", score=79),
    Mock(first_name="Bombardino", last_name="Crocodillo", info="Я Bombardino Crocodillo. Крокодил? Да. Бомба? Безусловно. Осторожно: я оба!", score=88),
]