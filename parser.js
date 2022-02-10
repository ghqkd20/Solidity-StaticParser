

const parser  = require("solidity-parser-antlr");
const fs = require('fs');

var file = process.argv[2]

const dat = fs.readFileSync(file,'utf8')

try {
    const ast = parser.parse(dat,{loc: true})
    const contracts = []
    parser.visit(ast, {
      ContractDefinition: node => {
        const contract = {
          name: node.name,
          methods: {},
          states: {}
        }
	console.log(JSON.stringify(node))
        parser.visit(node, {
          FunctionDefinition: node => {
            if (node.visibility === 'public') {
	console.log(JSON.stringify(node))
              contract.methods[node.name] = node
            }
		parser.visit(node,{
			FunctionCall : node => {
	console.log(JSON.stringify(node))
		},
			VariableDeclaration : node => {
	console.log(JSON.stringify(node))
			},
			ExpressionStatement : node => {
	console.log(JSON.stringify(node))
			},
			ForStatement : node =>{
	console.log(JSON.stringify(node))
			},
			IfStatement : node =>{
	console.log(JSON.stringify(node))
			}
		})
          },
	  ExpressionStatement: node => {
	console.log(JSON.stringify(node))
	},
          VariableDeclaration: node => {
	console.log(JSON.stringify(node))
          },
	  IfStatement: node =>{
	console.log(JSON.stringify(node))
		parser.visit(node,{
			ExpressionStatement : node => {
	console.log(JSON.stringify(node))
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
    }
  }
