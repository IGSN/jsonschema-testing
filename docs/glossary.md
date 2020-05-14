# IGSN 2040 Sprint Shared Glossary

## About
Some definitions of files that we can share so we are all on the same page.

## Terms

**registry**

description of registry here

**agents**

description of agents here

**aggregators**

description of aggregators here

**schema.org**

From the schema.org web site: *Schema.org vocabulary can be used with many different encodings, 
including RDFa, Microdata and JSON-LD. These vocabularies cover entities, relationships between
 entities and actions, and can easily be extended through a well-documented extension model.*   

**structured data on the web**

Where schema.org is one implementation of *structured data on the web*.  The approach is not
 limited to any given vocabulary like schema.org.  DCAT, FOAF, Dublin Core and other vocabulary 
 can be combined and used to present *structured data on the web*.

**JSON-LD**

This can be a confusing term.  It is often used in two main modes which are highly different.

def 1: JSON-LD is a serialization of the RDF Data model using JSON notation.

def 2: JSON-LD is sometimes used to represent the larger scope of structured data on the web, 
encoding instances using various vocabularies, like schema.org, into the JSON-LD serialization
 and placed in landing pages.   In this mode JSON-LD represents several concepts as a grouping.
    It is a confusing use of this term, but is not uncommon. 

**data graph**

Another term for the structured data on the web package.  Often this is the JSON-LD document 
embedded into a landing page.  However, that graph can be pulled, processed and converted to 
other formats.  The data graph term represents this information as a package in any form.  

**SHACL**

From the W3C information page: *SHACL Shapes Constraint Language, [is] a language for 
validating RDF graphs against a set of conditions. These conditions are provided as 
shapes and other constructs expressed in the form of an RDF graph. RDF graphs that are 
used in this manner are called "shapes graphs" in SHACL and the RDF graphs that are 
validated against a shapes graph are called "data graphs".* 

**JSON schema**

JSON Schema is a vocabulary that allows you to annotate and validate JSON documents.  
The JSON document being validated or described we call the instance, and the document 
containing the description is called the schema.

**shape graph**

Another term for the RDF graph that encodes SHACL constraints.  The shape graph is 
used by a SHACL tool to validate a data graph.

**context**

From the JSON-LD documentation on context: *Simply speaking, a context is used to map
 terms to IRIs. Terms are case sensitive and any valid string that is not a reserved 
 JSON-LD keyword can be used as a term.*

For our work the context will be a file referenced in the JSON-LD data graph via its 
context section.  It will map terms used to IRI (unique identifiers in graph space) 
for those terms.

**landing page**

description here

**web architecture**

description here


