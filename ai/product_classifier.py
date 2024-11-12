from typing import List, Dict, Callable, TypeVar
from langchain.prompts import PromptTemplate
from langchain_neo4j import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from functools import lru_cache
from prompts import create_classification_prompt_template, generate_classification_query
from models import create_classification_model
from utils import ProcessingResult

T = TypeVar('T')  # Input type
R = TypeVar('R')  # Result type

def create_lazy_pipeline(
    creator: Callable[[], Callable[[T], R]]
) -> Callable[[T], R]:
    """Create a lazy-loaded pipeline with caching."""

    @lru_cache(maxsize=1)
    def get_pipeline() -> Callable[[T], R]:
        return creator()

    def pipeline(input_data: T) -> R:
        return get_pipeline()(input_data)

    return pipeline

def create_graph(neo4j_url: str, neo4j_user: str, neo4j_password: str) -> Neo4jGraph:
    """Create a Neo4jGraph instance."""
    return Neo4jGraph(
        url=neo4j_url,
        username=neo4j_user,
        password=neo4j_password
    )

def create_cypher_chain(graph: Neo4jGraph, prompt: PromptTemplate) -> GraphCypherQAChain:
    """Create a GraphCypherQAChain."""
    model = create_classification_model()
    return GraphCypherQAChain.from_llm(
        llm=model,
        graph=graph,
        cypher_prompt=prompt,
        verbose=True
    )

def classify_product_string(cypher_chain: GraphCypherQAChain, graph: Neo4jGraph, product_string: str) -> Dict:
    """Classify a single product string."""
    schema = graph.get_schema()
    query = generate_classification_query(product_string, schema)
    result = cypher_chain.invoke(query)
    return result

def batch_classify_product_strings(
    neo4j_url: str, neo4j_user: str, neo4j_password: str, product_strings: List[str]
) -> List[Dict]:
    """Batch classify product strings."""
    graph = create_graph(neo4j_url, neo4j_user, neo4j_password)
    prompt = create_classification_prompt_template()
    cypher_chain = create_cypher_chain(graph, prompt)

    return [classify_product_string(cypher_chain, graph, ps) for ps in product_strings]

def create_product_classification_pipeline(
    neo4j_url: str, neo4j_user: str, neo4j_password: str
) -> Callable[[List[str]], List[Dict]]:
    """Create a lazy-loaded product classification pipeline."""

    @lru_cache(maxsize=1)
    def get_pipeline() -> Callable[[List[str]], List[Dict]]:
        return lambda product_strings: batch_classify_product_strings(
            neo4j_url, neo4j_user, neo4j_password, product_strings
        )

    return get_pipeline()
