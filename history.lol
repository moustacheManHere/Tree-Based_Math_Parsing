{"statements": {"Apple": "(2+(4*5))", "Mango": "((Apple+(Durian+(Pear*(Blueberry*(Coconut/Strawberry)))))/2)", "Pear": "(Apple*3)", "a": "diff_b(b+2*b+1)", "b": "(10+12)", "e": "diff_Apple(Apple+2)"}, "var": ["Apple", "Mango", "Pear", "a", "b", "e"], "trees": {"Apple": [["2", null, null], ["4", null, null], ["5", null, null], ["*", 1, 2], ["+", 0, 3]], "Mango": [["Apple", null, null], ["Durian", null, null], ["Pear", null, null], ["Blueberry", null, null], ["Coconut", null, null], ["Strawberry", null, null], ["/", 4, 5], ["*", 3, 6], ["*", 2, 7], ["+", 1, 8], ["+", 0, 9], ["2", null, null], ["/", 10, 11]], "Pear": [["Apple", null, null], ["3", null, null], ["*", 0, 1]], "a": [["1", null, null], ["2", null, null], ["1", null, null], ["*", 1, 2], ["0", null, null], ["b", null, null], ["*", 4, 5], ["+", 3, 6], ["0", null, null], ["+", 7, 8], ["+", 0, 9]], "b": [["10", null, null], ["12", null, null], ["+", 0, 1]], "e": [["1", null, null], ["0", null, null], ["+", 0, 1]]}, "results": {"Apple": 22, "Mango": null, "Pear": 66, "a": 3, "b": 22.0, "e": 1}}
3a4777a40630fca78eb59a4b698af1fb