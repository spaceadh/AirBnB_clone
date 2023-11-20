#!/usr/bin/python3
"""
    This module Defines the unittests cases for
    models/city.py.
"""
import os
import models
import unittest as u
from datetime import datetime
from time import sleep
from models.city import City


class Test_City_instantiation(u.TestCase):
    """
        Unittests cases for testing instantiation of the
        City class.
    """

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        ct = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(ct))
        self.assertNotIn("state_id", ct.__dict__)

    def test_name_is_public_class_attribute(self):
        ct = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(ct))
        self.assertNotIn("name", ct.__dict__)

    def test_two_cities_unique_ids(self):
        ct_1 = City()
        ct_2 = City()
        self.assertNotEqual(ct_1.id, ct_2.id)

    def test_two_cities_different_created_at(self):
        ct1 = City()
        sleep(0.10)
        ct2 = City()
        self.assertLess(ct1.created_at, ct2.created_at)

    def test_two_cities_different_updated_at(self):
        ct1 = City()
        sleep(0.10)
        ct2 = City()
        self.assertLess(ct1.updated_at, ct2.updated_at)

    def test_args_unused(self):
        ct = City(None)
        self.assertNotIn(None, ct.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        ct = City(id="246", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(ct.id, "246")
        self.assertEqual(ct.created_at, dt)
        self.assertEqual(ct.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class Test_City_save(u.TestCase):
    """
        Unittests cases for testing save method of the
        City class.
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        ct = City()
        sleep(0.10)
        first_updated_at = ct.updated_at
        ct.save()
        self.assertLess(first_updated_at, ct.updated_at)

    def test_two_saves(self):
        ct = City()
        sleep(0.10)
        first_updated_at = ct.updated_at
        ct.save()
        second_updated_at = ct.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.10)
        ct.save()
        self.assertLess(second_updated_at, ct.updated_at)

    def test_save_with_arg(self):
        ct = City()
        with self.assertRaises(TypeError):
            ct.save(None)


class Test_City_to_dict(u.TestCase):
    """
        Unittests cases for testing to_dict method of the
        City class.
    """

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        ct = City()
        self.assertIn("id", ct.to_dict())
        self.assertIn("created_at", ct.to_dict())
        self.assertIn("updated_at", ct.to_dict())
        self.assertIn("__class__", ct.to_dict())

    def test_to_dict_contains_added_attributes(self):
        ct = City()
        ct.middle_name = "Layi"
        ct.my_number = 45
        self.assertEqual("Layi", ct.middle_name)
        self.assertIn("my_number", ct.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        ct = City()
        ct_dict = ct.to_dict()
        self.assertEqual(str, type(ct_dict["id"]))
        self.assertEqual(str, type(ct_dict["created_at"]))
        self.assertEqual(str, type(ct_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        ct = City()
        ct.id = "246810"
        ct.created_at = ct.updated_at = dt
        tdict = {
            'id': '246810',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(ct.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        ct = City()
        self.assertNotEqual(ct.to_dict(), ct.__dict__)

    def test_to_dict_with_arg(self):
        ct = City()
        with self.assertRaises(TypeError):
            ct.to_dict(None)


if __name__ == "__main__":
    u.main()
