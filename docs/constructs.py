from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2

graph_attr = {
    "fontsize": "45",
    "bgcolor": "transparent",
    "pad": "1",
    "rankdir": "TB",
    # "concentrate": "true",
    "splines": "spline",
    "nodesep": "1.0",
    "ranksep": "1",
}

with Diagram("PACkit Library", show=False, graph_attr=graph_attr, direction="TB"):
    with Cluster("Basics") as basics_cluster:
      agent = EC2("Agent")
      prompt = EC2("Prompt")
      context = EC2("Context")
      toolbox = EC2("Toolbox")
      basics = [agent, prompt, context, toolbox]

    with Cluster("Constructs") as constructs_cluster:
      with Cluster("Groups"):
          panel = EC2("Panel")
          router = EC2("Router")


      with Cluster("Loops"):
          with Cluster("Single Agent"):
              retry = EC2("Retry")
              tool = EC2("Tool")


          with Cluster("Multiple Agents"):
              converse = EC2("Converse")
              extend = EC2("Extend")
              refine = EC2("Refine")
              team = EC2("Team")

    with Cluster("Results") as results_cluster:
       results = [
          EC2("Boolean"),
          EC2("Float"),
          EC2("Enum"),
          EC2("Int"),
          EC2("Function"),
          EC2("JSON"),
       ]

    # Groups
    # basics >> panel >> results
    # basics >> router >> results

    # Single Agent Loops
    # basics  >> retry >> results
    # basics >> tool >> results

    # Multiple Agent Loops
    # basics >> converse >> results
    # basics >> extend >> results
    # basics >> refine >> results
    # basics >> team >> results
