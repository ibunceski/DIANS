package mk.ukim.finki.dians.hw2backend.web;

import mk.ukim.finki.dians.hw2backend.model.IssuerData;
import mk.ukim.finki.dians.hw2backend.model.IssuerDates;
import mk.ukim.finki.dians.hw2backend.service.IssuerDataService;
import mk.ukim.finki.dians.hw2backend.service.IssuerDatesService;
import mk.ukim.finki.dians.hw2backend.service.PythonScriptService;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://192.168.225.84:3000")
public class StockController {

    final IssuerDataService issuerDataService;
    final IssuerDatesService issuerDatesService;
    final PythonScriptService pythonScriptService;

    public StockController(IssuerDataService issuerDataService, IssuerDatesService issuerDatesService, PythonScriptService pythonScriptService) {
        this.issuerDataService = issuerDataService;
        this.issuerDatesService = issuerDatesService;
        this.pythonScriptService = pythonScriptService;
    }

    @GetMapping("/issuers")
    public List<String> getAllIssuers() {
        return issuerDataService.getAllIssuers();
    }

    @GetMapping("/issuer-data")
    public List<IssuerData> getAllIssuerData() {
        return issuerDataService.getAllData();
    }


    @GetMapping("/issuer-data/{issuer}")
    public List<IssuerData> getDataByIssuer(@PathVariable String issuer) throws InterruptedException {
        Thread.sleep(1000); // for the loading animation to be shown on the front end
        return issuerDataService.getDataByIssuer(issuer);
    }


    @GetMapping("/issuer-dates/{issuer}")
    public Optional<IssuerDates> getIssuerLastDate(@PathVariable String issuer) {
        return issuerDatesService.getLastDateForIssuer(issuer);
    }

    @GetMapping("/fill-data")
    public void checkData(){
        pythonScriptService.executePythonScript();
    }
}

