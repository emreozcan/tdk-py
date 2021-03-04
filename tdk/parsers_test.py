from .parsers import parse_autocomplete_index


class TestAutocompleteIndexParser:
    def test_extraction(self):
        expected_output = ["avize", "safran", "tabela"]
        function_input = [{"madde": x} for x in expected_output]
        assert expected_output == parse_autocomplete_index(function_input)

    def test_alphabetical_order(self):
        expected_output = ["avize", "safran", "tabela"]
        function_input = [{"madde": x} for x in expected_output[::-1]]  # Flipped list
        assert expected_output == parse_autocomplete_index(function_input)
