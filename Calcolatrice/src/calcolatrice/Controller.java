package calcolatrice;

import com.jfoenix.controls.JFXHamburger;
import com.jfoenix.controls.JFXListView;
import com.jfoenix.controls.JFXPopup;
import com.jfoenix.controls.JFXPopup.PopupHPosition;
import com.jfoenix.controls.JFXPopup.PopupVPosition;
import com.jfoenix.controls.JFXRippler;
import java.util.Date;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.geometry.Insets;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.AnchorPane;
import javax.script.ScriptException;

public class Controller {

    Thread capo;
    String s = "";
    calc c = new calc();
    @FXML
    private AnchorPane cron;
    @FXML
    private JFXPopup cronpop;
    @FXML
    private JFXListView listcron;
    @FXML
    private JFXHamburger burger1;
    @FXML
    private Button btnCA;
    @FXML
    private AnchorPane funzioni;
    @FXML
    private AnchorPane anc;
    @FXML
    private JFXRippler rip;
    @FXML
    private JFXPopup popup;
    @FXML
    private TextField txtExp;

    private double timer = 0;

    @FXML
    protected void initialize() throws InterruptedException {

        capo = new Thread(() -> {
            try {
                control();
            } catch (InterruptedException ex) {
            }
        });

        capo.start();

        burger1.setPadding(new Insets(10, 5, 10, 5));
        rip.setControl(burger1);
        rip.setMaskType(JFXRippler.RipplerMask.CIRCLE);
        rip.setPostion(JFXRippler.RipplerPos.BACK);
        popup.setContent(funzioni);
        popup.setSource(burger1);
        listcron.depthProperty().set(1);

        burger1.setOnMouseClicked((e) -> {
            popup.show(PopupVPosition.BOTTOM, PopupHPosition.RIGHT);
            burger1.getAnimation().setRate(burger1.getAnimation().getRate() * -1);
            burger1.getAnimation().play();

        });
        cronpop.setContent(cron);
        cronpop.setSource(burger1);

        txtExp.setOnMouseDragged((e) -> {
            cronpop.show(PopupVPosition.TOP, PopupHPosition.RIGHT);

        });
        listcron.setOnMouseDragged((e) -> {
            cronpop.close();
        });

        listcron.getSelectionModel().selectedItemProperty().addListener(new ChangeListener<Label>() {       //assegno un evento a tutti gli elementi della lista

            @Override
            public void changed(ObservableValue<? extends Label> observable, Label oldValue, Label newValue) {  //Gestione della Cronologia
                String exp = newValue.getText();
                if (!exp.matches("[=][' ']([0-9]+[.][0-9]+)?")) {

                    while (!exp.matches("[=][' ']([0-9]+[.][0-9]+)?")) {
                        exp = exp.substring(1, exp.length());
                    }
                    exp = exp.substring(2, exp.length());
                    txtExp.setText(txtExp.getText() + " " + exp);

                    cronpop.close();
                }
            }

        });
    }

    private void control() throws InterruptedException {
        while (true) {
            Thread.sleep(1000);
            if (funzioni.impl_isTreeVisible()) {
                while (funzioni.impl_isTreeVisible()) {
                    Thread.sleep(250);
                }

                burger1.getAnimation().setRate(burger1.getAnimation().getRate() * -1);
                burger1.getAnimation().play();
            }
        }
    }
    
    @FXML
    void canc() {
        txtExp.setText("");
    }

    @FXML
    void onClick(ActionEvent event) throws ScriptException {

        s = txtExp.getText();
        String butt = (((Button) event.getSource()).getText());
        if ("=".equals(butt)) {
            String a = txtExp.getText();
            Object[] o;
            o = a.split(" ");
            Object risultato=c.esegui(o);
            String ris="";
            if (risultato instanceof String) {
                ris=(String)risultato;
            }
            else{
                ris=String.valueOf(risultato);
            }
            txtExp.setText(ris);
            Label lab = new Label(a + " = " + ris);

            listcron.getItems().add(lab);
        }else if(butt.equals("C")){
            canc();

        } else if (butt.equals("CA")) {

            if (s.length() > 0) {
                boolean bol = false;
                if (s.length() > 2) {
                    bol = s.charAt(s.length() - 2) == ' ';
                }
                if (!bol) {

                    txtExp.setText(s.substring(0, s.length() - 1));
                } else {
                    txtExp.setText(s.substring(0, s.length() - 2));
                }
            }

            
        } else if ((butt.matches("[-]") && ((txtExp.getText().length()==0) || ((txtExp.getText().length()>2)&&(((txtExp.getText().charAt(txtExp.getText().length() - 2) + "")).matches("[+*/(]")))))) {//per gestire il meno 
            txtExp.setText(txtExp.getText() + "-");                                                
        } else if (((Button) event.getSource()).getText().matches("[-+/*]")) {                  
            txtExp.setText(txtExp.getText() + " " + ((Button) event.getSource()).getText() + " ");
        } else if (((Button) event.getSource()).getText().matches("[π]")) {
            txtExp.setText(txtExp.getText() + (Double.toString(Math.PI)));
        } else if (((Button) event.getSource()).getText().matches("['(']")) {
            txtExp.setText(txtExp.getText() + " " + ((Button) event.getSource()).getText() + " ");
        } else if (((Button) event.getSource()).getText().matches("[')']")) {
            txtExp.setText(txtExp.getText() + " " + ((Button) event.getSource()).getText() + " ");
        } else if (((Button) event.getSource()).getText().matches("Sin|Cos|log|ln")) {
            txtExp.setText(txtExp.getText() + ((Button) event.getSource()).getText() + " ( ");
        } else if (((Button) event.getSource()).getText().matches("√")) {
            txtExp.setText(txtExp.getText() + "sqrt ( ");
        } else {

            txtExp.setText(txtExp.getText() + ((Button) event.getSource()).getText());

        }

    }
}
