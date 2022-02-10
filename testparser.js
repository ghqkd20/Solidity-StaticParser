

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
	console.log(node)
        parser.visit(node, {
          FunctionDefinition: node => {
            if (node.visibility === 'public') {
contract.methods[node.name] = node
            }
		console.log(node)
		parser.visit(node,{
			FunctionCall : node => {
			console.log(node)
		},
			VariableDeclaration : node => {
				console.log(node)
			},
			ExpressionStatement : node => {
				console.log(node)
			},
			ForStatement : node =>{
				console.log(node)
			},
			IfStatement : node =>{
				console.log(node)
			}
		})
          },
	  ExpressionStatement: node => {
		console.log(node)
	},
          VariableDeclaration: node => {
		console.log(node)
          },
	  IfStatement: node =>{
		console.log(node)
		parser.visit(node,{
			ExpressionStatement : node => {
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
    }
  }
