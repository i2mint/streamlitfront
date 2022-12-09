"""
When strategizing, one can often be faced with making choices that have different
effects on the short and long term.

In this particular case, we're referring to the "cost of inflexibility" which is often
ignored when making decisions.

If we believe that "change is the only constant" (Heraclitus), one should prepare for
this inevitable by considering flexibility as a top characteristic of a plan.

The model proposed above is simple, yes, but I would argue that an explicit,
even if simplistic, model is often more useful than the implicit models that underlie
most of our decisions.

The model is of course binary: "failure effort" can defined by "efforts that DID NOT
contribute towards success" and "success effort" can be defined by "efforts that DID
contribute towards success". You might point out that, in fact, there's a lot of grey
area, and that past failures contribute to future successes. And I'd agree.
A lot of capital can be created in past failures.

To accommodate for this perspective, we could enhance the model with that important
aspect of reuse between "failure efforts" and "success efforts".

"""

from meshed import code_to_dag
from operator import add, mul, sub


def compute_failure_effort_amount(success_effort_amount):
    return 1 - success_effort_amount


@code_to_dag(func_src=locals())
def costing_inflexibility():
    #     failure_effort_amount = compute_failure_effort_amount(success_effort_amount)
    wasted_cost = mul(failure_effort_cost, failure_effort_amount)
    success_cost = mul(success_effort_cost, success_effort_amount)
    cost = add(wasted_cost, success_cost)
    profit = sub(revenue, cost)


# costing_inflexibility.dot_digraph()


# def compute_cost(
#         success_effort_cost,
#         success_effort_amount=0.2,
#         failure_effort_cost=None,
#         failure_effort_amount=None,
# ):
#     # if failure cost not given, make it be the same as success cost
#     failure_effort_cost = failure_effort_cost or success_effort_cost
#     if failure_effort_amount is None:
#         if 0 <= success_effort_amount <= 1:
#             # if success_effort_amount was measured as proportion, failure is the reste
#             failure_effort_amount = 1 - success_effort_amount
#         else:
#             # if not, assume the success rate is 10%, so
#             failure_effort_amount = success_effort_amount * 9
#     return (
#             success_effort_amount * success_effort_cost
#             + failure_effort_amount * failure_effort_cost
#     )
