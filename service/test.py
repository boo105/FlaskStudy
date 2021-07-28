from flask import request
from flask_restx import Resource, Api, Namespace, fields

Good = Namespace(
    name="Good",
    description="Good 테스트용 API.",
)

# REST Api에 이용할 데이터 모델을 정의한다
model_goods = Good.model('row_goods', {
    'id': fields.Integer(readOnly=True, required=True, description='상품번호', help='상품번호는 필수'),
    'goods_name': fields.String(required=True, description='상품명', help='상품명은 필수')
})

class GoodsDAO(object):
    '''상품정보 Data Access Object'''
    def __init__(self):
        self.counter = 0
        self.rows    = []

    def get(self, id):
        '''id를 이용하여 상품정보 조회한다'''
        for row in self.rows:
            if row['id'] == id:
                return row
        #api.abort(404, "{} doesn't exist".format(id))
        return f"{id}가 존재 하지 않음",404

    def create(self, data):
        '''신규 상품을 등록한다'''
        row = data
        row['id'] = self.counter = self.counter + 1
        self.rows.append(row)
        return row

    def update(self, id, data):
        '''입력 id의 data를 수정한다'''
        row = self.get(id)
        row.update(data)
        return row

    def delete(self, id):
        '''입력 id의 data를 삭제한다'''
        row = self.get(id)
        self.rows.remove(row)

DAO = GoodsDAO() # DAO 객체를 만든다
DAO.create({'goods_name': '삼성 노트북 9'}) # 샘플 1 데이터 만든다
DAO.create({'goods_name': 'LG 노트북 gram'}) # 샘플 2 데이터 만든다


@Good.route('/') # 네임스페이스 x.x.x.x/goods 하위 / 라우팅
class GoodsListManager(Resource):
    @Good.marshal_list_with(model_goods)
    def get(self):
        '''전체 리스트 조회한다'''
        return DAO.rows

    @Good.expect(model_goods)
    @Good.marshal_with(model_goods, code=201)
    def post(self):
        '''새로운 id 추가한다'''
        # request.json[파라미터이름]으로 파라미터값 조회할 수 있다
        data = request.get_json()
        print("post data : ")
        print(data)
        return DAO.create(data), 201

@Good.route('/<int:id>') # 네임스페이스 x.x.x.x/goods 하위 /숫자 라우팅
@Good.response(404, 'id를 찾을 수가 없어요')
@Good.param('id', '상품번호를 입력해주세요')
class GoodsRUDManager(Resource):
    @Good.marshal_with(model_goods)
    def get(self, id):
        '''해당 id 상품정보를 조회한다'''
        return DAO.get(id)

    def delete(self, id):
        '''해당 id 삭제한다'''
        DAO.delete(id)
        return '', 200

    @Good.expect(model_goods)
    @Good.marshal_with(model_goods)
    def put(self, id):
        '''해당 id 수정한다'''
        data = request.get_json()
        return DAO.update(id, data)