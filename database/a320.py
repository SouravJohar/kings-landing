a320 = {
    "fclass": {
        "info": {
            "f": {
                "category": "First Class",
                "price": 0,
                "classes": "first-class"
            }
        },
        "map": ["f__f__", "__f__f", "f__f__", "__f__f", "f__f__", "__f__f", "f__f__", "__f__f", "f__f__", "__f__f"],
        "legend": [
            ["f", "available", "First Class"],
            ["f", "unavailable", "Already Booked"]
        ],
        "columns": ["V", "V", "V", "X", "V", "X"]
    },
    "business": {
        "info": {
            "n": {
                "category": "Business",
                "price": 0,
                "classes": "economy-class-con"
            },
            "f": {
                "category": "Business - Recliners",
                "price": 500,
                "classes": "first-class"
            }
        },
        "map": ["ff_ff", "nn_nn", "nn_nn", "nn_nn", "nn_nn", "nn_nn", "nn_nn", "f___f"],
        "legend": [
            ["f", "available", "Extra Reclining - Rs 500"],
            ["n", "available", "Standard - no extra cost"],
            ["", "unavailable", "Already Booked"]
        ],
        "columns": ["S", "T", "", "U", "V"]
    },
    "num_economy": 150,
    "num_fclass": 20,
    "num_business": 30,
    "economy": {
        "info": {
            "a": {
                "category": "Economy - Extra Legroom",
                "price": 200,
                "classes": "first-class"
            },
            "n": {
                "category": "Economy",
                "price": 0,
                "classes": "economy-class"
            },
            "f": {
                "category": "Economy - Convineant",
                "price": 100,
                "classes": "economy-class-con"
            }
        },
        "map": ["aaa_aaa", "aaa_aaa", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fff_fff", "fff_fff", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fnf_fnf", "fnf_fnf", "nnn_nnn", "nnn_nnn", "nnn_nnn"],
        "legend": [
            ["a", "available", "Extra Legroom - Rs 200"],
            ["n", "available", "Standard - no extra cost"],
            ["f", "available", "Convineant seats - Rs100"],
            ["f", "unavailable", "Already Booked"]
        ],
        "columns": ["A", "B", "C", "", "D", "E", "F"]
    }
}
