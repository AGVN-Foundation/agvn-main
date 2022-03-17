## Tests need to be changed
Since this project uses `pytest` on django models, the tests for the objects
must be of the form e.g. `Model.objects.all()`.
Some models should have `create()` methods to instantiate a class for quick testing as well.
