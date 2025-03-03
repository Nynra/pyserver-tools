class ModelTestBase:
    """
    Base class for testing django models.

    This class should be inherited by all model test cases and
    expects the following attributes to be set:
    - model_class: The model class that should be tested
    - search_key: The key that should be used to search for the
        database entry

    This class does not implement a setup method. The child class
    should implement this method and set the following attributes:
    - self.data: The data that should be used for testing
    - self.model: The model instance that should be
        tested
    """

    model_class = None
    search_key = None

    @classmethod
    def setUpClass(cls):
        """Check if the child class has set the required attributes."""
        super().setUpClass()
        if cls.model_class is None:
            raise NotImplementedError("The model_class attribute must be set.")
        if cls.search_key is None:
            raise NotImplementedError("The search_key attribute must be set.")

    def test_attributes(self):
        """Test if the model has the correct attributes."""
        for key in self.data.keys():
            self.assertEqual(
                getattr(self.model, key),
                self.data[key],
                "Attribute {} is not correct, expected {}, got {}".format(key, self.data[key], getattr(self.model, key)),
            )

    def test_create(self):
        """Test if the model can create a new database entry."""
        search_kwargs = {self.search_key: self.data[self.search_key]}
        self.assertTrue(self.model_class.objects.filter(**search_kwargs).exists())

        # Check if the attributes are correct
        model = self.model_class.objects.get(**search_kwargs)
        for key in self.data.keys():
            self.assertEqual(
                getattr(model, key),
                self.data[key],
                "Attribute {} is not correct, expected {}, got {}".format(key, self.data[key], getattr(model, key)),
            )
