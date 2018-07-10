package calcolatrice;

/**
 *
 * @author Andrea
 */
public class op {

    String op;
    int precedenza;

    public op(String op) {
        this.op = op;
        if (op.matches("[/*]")) {
            precedenza = 1;
        } else if (op.matches("[+-]")) {
            precedenza = 0;
        } else if (op.matches("['()']")) {
            precedenza = 2;
        }
        else if(op.matches("Sin|Cos|log|ln|sqrt")) {
            precedenza=2;
            
        }

    }

    public boolean HasHigherPrec(op op2) {
        return (precedenza - op2.precedenza) > 0;

    }
    public boolean aperta(){
        return op.equals("(");
    }
}
