const parser  = require("solidity-parser-antlr");
console.log("hii")
try {
    const ast = parser.parseFile("./target/integer.sol")
   console.log("hi") 
	console.log(ast)
    const contracts = []
    parser.visit(ast, {
      ContractDefinition: node => {
        const contract = {
          name: node.name,
          methods: {},
          states: {}
        }
	console.log(node)
        parser.visit(node, {
          FunctionDefinition: node => {
            if (node.visibility === 'public') {
		console.log(node)
              contract.methods[node.name] = node
            }
		parser.visit(node,{
			FunctionCall : node => {
				console.log(node)
		},
			VariableDeclaration : node => {
				console.log(node)
				parser.visit(node, {
					FunctionCall : node => {
						console.log(node)
					}
				})
			},
			Expression : node => {
				console.log(node)
			},
			ForStatement : node =>{
				console.log(node)
				parser.visit(node,{
					TypeName : node =>{
						console.log(node)
					}
				})
			}
		})
          },
	  ExpressionStatement: node => {
		console.log(node)
	},
          VariableDeclaration: node => {
            if (node.visibility === 'public' && node.isStateVar) {
             console.log(node) 
		contract.states[node.name] = node
            }
		console.log(node)
          },
	  IfStatement: node =>{
		console.log(node)
		parser.visit(node,{
			Expression : node => {
				console.log(node)
			}
		})
	}
        })
        contracts.push(contract)
      }
    })
//    console.log(contracts)
    return contracts
  } catch (e) {
    if (e instanceof parser.ParserError) {
      console.log(e.errors)
	console.log("error")
    }
  }
