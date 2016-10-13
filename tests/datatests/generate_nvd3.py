import os

# success = open(name_success_file)
# wrong = open(name_wrong_file)

name_success_file = './src/output_correct.tsv'
name_wrong_file = './src/output_incorrect.tsv'

with open(name_success_file) as f:
    number_success = sum(1 for _ in f)

with open(name_wrong_file) as f:
    number_wrong = sum(1 for _ in f)

chart1 = [{
            'key' : 'success',
            'values' : [
                {'x' : 'success', 'y' : number_success },
                {'x' : 'wrong', 'y' : 0 }
            ]
        },
        {
            'key' : 'wrong',
            'values' : [
                {'x' : 'success', 'y' : 0 },
                {'x' : 'wrong', 'y' : number_wrong }
            ]
        }]

with open(name_success_file) as f:
    number_success_cross_ref = sum(1 for line in f if line.split('\t')[0] == 'CrossRef')
    number_success_mendeley = sum(1 for line in f if line.split('\t')[0] == 'Mendeley')

chart2 = [{
            'key' : 'success_cross_ref',
            'values' : [
                {'x' : 'success_mendeley', 'y' : 0 },
                {'x' : 'success_cross_ref', 'y' : number_success_cross_ref },
                {'x' : 'wrong', 'y' : 0 }
            ]
        },
        {
            'key' : 'success_mendeley',
            'values' : [
                {'x' : 'success_mendeley', 'y' : number_success_mendeley },
                {'x' : 'success_cross_ref', 'y' : 0 },
                {'x' : 'wrong', 'y' : 0 }
            ]
        },
        {
            'key' : 'wrong',
            'values' : [
                {'x' : 'success_mendeley', 'y' : 0 },
                {'x' : 'success_cross_ref', 'y' : 0 },
                {'x' : 'wrong', 'y' : number_wrong }
            ]
        }]

# chart2 = [{
#     'key' : 'success vs wrong',
#     'values' : [
#         {'label' : 'success_cross_ref', 'value' : number_success_cross_ref },
#         {'label' : 'success_mendeley', 'value' : number_success_mendeley },
#         {'label' : 'wrong', 'value' : number_wrong }
#     ]
# }]

interval = 1
def cround_rating(rating):
    return (100 - interval) if rating == 1 else rating*100//interval*interval
    # if rating < 0.2:
    #     return 0
    # if rating < 0.5:
    #     return 20
    # if rating < 0.8:
    #     return 50
    # if rating < 0.9:
    #     return 80
    # return 90

number_success = {}
with open(name_success_file) as f:
    for line in f:
        vals = line.split('\t')
        rating = float(vals[3])
        round_rating = cround_rating(rating)
        number_success[round_rating] = number_success.get(round_rating, 0) + 1

number_wrong = {}
with open(name_wrong_file) as f:
    for line in f:
        vals = line.split('\t')
        rating = float(vals[3])
        round_rating = cround_rating(rating)
        number_wrong[round_rating] = number_wrong.get(round_rating, 0) + 1

chart3 = [{
    'key' : 'success',
    'values' : [{
            'x' : "%d%% - %d%%" % (x,x+interval),
            'y' : number_success.get(x, 0)
        } for x in [interval*x for x in range(100//interval)]]
    },{
    'key' : 'wrong',
    'values' : [{
            'x' : "%d%% - %d%%" % (x,x+interval),
            'y' : number_wrong.get(x, 0)
        } for x in [interval*x for x in range(100//interval)]]
}]

print(chart1)
print(chart2)
print(chart3)
