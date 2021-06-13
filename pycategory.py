class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'train', 'texi']], \
        'income', ['salary', 'bonus']]
    
    def view(self):
        """Print out all categories with indentation."""
        def view_inner(cats, level = -1):
            if cats == None:
                return
            if type(cats) == list:
                for child in cats:
                    view_inner(child, level + 1)
            else:
                print(f'{" " * 2 * level}・{cats}')
        view_inner(self._categories)
    
    def is_category_valid(self, desired_category):
        """Check if the user-input category is valid."""
        def is_category_valid_inner(category, categories):
            if type(categories) == list:
                for child in categories:
                    ret =  is_category_valid_inner(category, child)
                    if ret == True:
                        return is_category_valid_inner(category, child) # exit this function
            elif type(categories) == str:
                return str(category) == str(categories)
        return is_category_valid_inner(desired_category, self._categories)

    def find_subcategories(self, desired_categories):
        """Find sub categories of a specific category."""
        def find_subcategories_gen(category, categories, found = False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories)\
                        and type(categories[index + 1]) == list:
                        yield from find_subcategories_gen(category, categories[index + 1], True)
            else:
                if categories == category or found == True:
                    yield categories
        return [i for i in find_subcategories_gen(desired_categories, self._categories)]