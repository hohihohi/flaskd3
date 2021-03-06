from flaskd3.externals.mysql import DataSourceRepository, ObjectRepository
from tests.externals.mysql import *


def test_find_by_id(ormapper, valid_data_source, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        data_source_repository = DataSourceRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        obj = object_repository.save(obj)
        data_source = valid_data_source.copy()
        data_source.object = obj
        expect = data_source_repository.save(data_source)
        # call method to test
        actual = data_source_repository.find_by_id(expect.id)
        data_source_assertions(expect, actual)


def test_find_by_name(ormapper, valid_data_source, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        data_source_repository = DataSourceRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        obj = object_repository.save(obj)
        data_source = valid_data_source.copy()
        data_source.object = obj
        expect = data_source_repository.save(data_source)
        # call method to test
        actual = data_source_repository.find_by_name(expect.name)
        data_source_assertions(expect, actual)


def test_find_by_user_id(ormapper, valid_data_source, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        data_source_repository = DataSourceRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj_1 = valid_object.copy()
        obj_1.bucket = bucket
        obj_1 = object_repository.save(obj_1)
        obj_2 = valid_object.copy()
        obj_2.bucket = bucket
        obj_2.name = 'test_data_source2'
        obj_2 = object_repository.save(obj_2)
        ds_1 = valid_data_source.copy()
        ds_1.object = obj_1
        ds_1 = data_source_repository.save(ds_1)
        ds_2 = valid_data_source.copy()
        ds_2.object = obj_2
        ds_2.name = obj_2.name
        ds_2 = data_source_repository.save(ds_2)
        expect = [ds_2, ds_1]
        # call method to test
        actual = data_source_repository.find_by_user_id(valid_object.user_id)
        data_source_list_assertions(expect, actual)


def test_save(ormapper, valid_data_source, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        data_source_repository = DataSourceRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        obj = object_repository.save(obj)
        expect = valid_data_source.copy()
        expect.object = obj
        # call method to test
        actual = data_source_repository.save(expect)
        assert actual.id is not None and actual.id >= 0
        assert expect.user_id == actual.user_id
        assert expect.name == actual.name
        object_assertions(expect.object, actual.object)
        assert expect.data_type == actual.data_type
        assert expect.created_at < actual.created_at
        assert expect.updated_at < actual.updated_at


def test_save_with_duplicate_error(ormapper, valid_data_source, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        data_source_repository = DataSourceRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj_1 = valid_object.copy()
        obj_1.bucket = bucket
        obj_1 = object_repository.save(obj_1)
        obj_2 = valid_object.copy()
        obj_2.bucket = bucket
        obj_2.name = 'test_data_source2'
        obj_2 = object_repository.save(obj_2)
        ds_1 = valid_data_source.copy()
        ds_1.object = obj_1
        _ = data_source_repository.save(ds_1)
        ds_2 = valid_data_source.copy()
        ds_2.object = obj_2
        # call method to test
        expect = 'Invalid parameter duplicate error occurred: DataSource'
        actual = data_source_repository.save(ds_2)
        assert expect == str(actual)


def test_delete(ormapper, valid_data_source, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        data_source_repository = DataSourceRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        obj = object_repository.save(obj)
        data_source = valid_data_source.copy()
        data_source.object = obj
        expect = data_source_repository.save(data_source)
        # call method to test
        actual = data_source_repository.delete(expect)
        data_source_assertions(expect, actual)


def test_delete_with_non_exist_data_source(ormapper, valid_data_source, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        data_source_repository = DataSourceRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        obj = object_repository.save(obj)
        data_source = valid_data_source.copy()
        data_source.object = obj
        # call method to test
        expect = f'Cannot delete data source because it was not found: {data_source.name}'
        actual = data_source_repository.delete(data_source)
        assert expect == str(actual)


def test_update(ormapper, valid_data_source, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        data_source_repository = DataSourceRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        obj = object_repository.save(obj)
        data_source = valid_data_source.copy()
        data_source.object = obj
        expect = data_source_repository.save(data_source)
        expect.name = 'test_data_source2'
        # call method to test
        actual = data_source_repository.update(expect)
        data_source_assertions(expect, actual)


def test_update_with_unique_restriction_error(ormapper, valid_data_source, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        data_source_repository = DataSourceRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj_1 = valid_object.copy()
        obj_1.bucket = bucket
        obj_1 = object_repository.save(obj_1)
        obj_2 = valid_object.copy()
        obj_2.bucket = bucket
        obj_2.name = 'test_data_source2'
        obj_2 = object_repository.save(obj_2)
        ds_1 = valid_data_source.copy()
        ds_1.object = obj_1
        _ = data_source_repository.save(ds_1)
        ds_2 = valid_data_source.copy()
        ds_2.object = obj_2
        ds_2.name = obj_2.name
        ds_2 = data_source_repository.save(ds_2)
        ds_2.name = ds_1.name
        # call method to test
        expect = 'Invalid parameter duplicate error occurred: DataSource'
        actual = data_source_repository.update(ds_2)
        assert expect == str(actual)


def test_update_with_non_exist_data_source(ormapper, valid_data_source, valid_object, valid_bucket):
    with ormapper.create_session() as session:
        delete_record_from_database(session)
        object_repository = ObjectRepository(session)
        data_source_repository = DataSourceRepository(session)
        # save data
        bucket = object_repository.save_bucket(valid_bucket)
        obj = valid_object.copy()
        obj.bucket = bucket
        obj = object_repository.save(obj)
        data_source = valid_data_source.copy()
        data_source.object = obj
        # call method to test
        expect = f'Cannot update data source because it was not found: {data_source.name}'
        actual = data_source_repository.update(data_source)
        assert expect == str(actual)
