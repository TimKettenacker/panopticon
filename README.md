# panopticon
My view on data has been shaped by my experiences with master data management and data quality initiatives. At its core, records need to be linked given on fuzzy attributes and contents to distill a unique identity of what we want to look at. Therefor, data has to be compared and grouped based on a given set of criteria. Now social media has a somewhat deserved reputation of displaying very openly how transparent we have become. Combined with the rising omni-availability and popularity of those channels, it is a rather obvious choice to use social media platforms for entity resolution.

In the approach depicted here, I am using Neo4j to map twitter entities to get a grasp on that topic. The twitter api comes with the benefit to focus on one specific event and links users come up with to its surroundings. I was sniffing other apis, like instagram for example, but found them rather clumsy to deal with for my purpose.      

After querying twitter on a controversial event, data needs to be shaped into a common format to complete this task. Here, both is done in python. After that, it is loaded into neo4j.
