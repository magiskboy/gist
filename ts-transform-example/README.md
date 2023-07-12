## Typescript transform API in typescript compiler

A demo for removing `console.log` from production code.

```typescript
import ts, { SyntaxKind } from "typescript";

const source = `
function fib(n: number): number {
  if (n < 2) return n;
  return fib(n - 2) + fib(n - 1);
}
console.log("foo");
const n = 10;
const ret = fib(n);
console.log(\`fib(\${n}) = \${ret}\`);
`;

function transformerFactory<T extends ts.Node>(): ts.TransformerFactory<T> {
  return (context) => {
    const { factory } = context;
    const transform: ts.Visitor = (node) => {
      if (
        node.kind === SyntaxKind.CallExpression &&
        (node as ts.CallExpression).expression.getText() === "console.log"
      ) {
        return factory.createVoidExpression(factory.createNumericLiteral("0"));
      }
      return ts.visitEachChild(node, (node) => transform(node), context);
    };
    return (node: T) => ts.visitNode(node, transform);
  };
}

const result = ts.transpileModule(source, {
  compilerOptions: { module: ts.ModuleKind.CommonJS },
  transformers: { before: [transformerFactory()] },
});

console.log(result.outputText);
```
