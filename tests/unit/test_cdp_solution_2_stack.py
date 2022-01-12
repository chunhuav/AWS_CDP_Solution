import aws_cdk as core
import aws_cdk.assertions as assertions

from cdp_solution_2.cdp_solution_2_stack import CdpSolution2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdp_solution_2/cdp_solution_2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdpSolution2Stack(app, "cdp-solution-2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
