package calcolatrice;

import java.util.ArrayList;
import java.util.Stack;

/**
 *
 * @author Andrea
 */
public class calc {
    
    public calc() {
        
    }

    private Object valuta(ArrayList o) {    //da polacca a risultato
        Stack<Object> s = new Stack<Object>();
        try{
        
        for (int i = 0; i < o.size(); i++) {
            String temp = (String) o.get(i);
            if (temp.matches("[-]?[0-9]+([.][0-9]+)?")) {
                s.push(temp);
            } else if (temp.matches("[-*/+]")) {
                String op1 = (String) s.pop();
                String op2 = (String) s.pop();
                String ris = val(temp, op1, op2);
                s.push(ris);
            } else if (temp.matches("Sin|Cos|log|ln|sqrt")) {
                String op01 = (String) s.pop();
                String ris1 = val(temp, op01);
                s.push(ris1);

            }
        }
        }
        catch (Exception ex) {
            return "Errore";
        }
        return Double.parseDouble((String) s.peek());

    }

    private ArrayList polacca(Object[] o) { //da token di Stringa a notazione polacca
        ArrayList polacca = new ArrayList();

        Stack<op> op = new Stack();
        int i = 0;
        while (i < o.length) {

            String temp = (String) o[i];
            if (temp.matches("[-]?[0-9]+([.][0-9]+)?")) {
                polacca.add(temp);
            } else if (temp.matches("(Sin|Cos|log|sqrt|ln|[-*/+]+)")) {
                while (!op.empty() && !op.peek().aperta() && op.peek().HasHigherPrec(new op(temp))) {
                    polacca.add(op.peek().op);
                    op.pop();
                }
                op.push(new op(temp));

            } else if (temp.equals("(")) {
                op.push(new op(temp));

            } else if (temp.equals(")")) {
                while (!op.empty() && !op.peek().aperta()) {
                    polacca.add(op.peek().op);
                    op.pop();
                }
                op.pop();
            }

            i++;
        }
        while (!op.empty()) {
            polacca.add(op.pop().op);

        }
        return polacca;
    }

    private String val(String operazione, String op1, String op2) { //valuta due operandi e un operatore
        Double b = Double.parseDouble(op1);
        Double a = Double.parseDouble(op2);
        Double ris = 0.0;
        switch (operazione) {
            case "/":
                ris = a / b;
                break;
            case "-":
                ris = a - b;
                break;
            case "*":
                ris = a * b;
                break;
            case "+":
                ris = a + b;
                break;
                
        }
        return String.valueOf(ris);
    }

    private String val(String operazione, String op1) { //valuta un operando e un operatore
        Double a = Double.parseDouble(op1);
        Double ris = 0.0;
        switch (operazione) {
            case "Sin":
                ris = Math.sin(a);
                break;
            case "Cos":
                ris = Math.cos(a);
                break;
            case "sqrt":
                ris = Math.sqrt(a);
                break;
            case "log":
                ris = Math.log10(a);
                break;
            case "ln":
                ris = Math.log(a);
                break;
                
        }
        return String.valueOf(ris);
    }
    public Object esegui(Object[] o){   //Data un espressione matematica restituisco il risultato
        return valuta(polacca(o));
        
    }
}