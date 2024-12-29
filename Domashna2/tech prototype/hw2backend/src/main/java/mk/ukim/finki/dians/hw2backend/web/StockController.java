package mk.ukim.finki.dians.hw2backend.web;

import mk.ukim.finki.dians.hw2backend.model.IssuerData;
import mk.ukim.finki.dians.hw2backend.model.IssuerDates;
import mk.ukim.finki.dians.hw2backend.service.IssuerDataService;
import mk.ukim.finki.dians.hw2backend.service.IssuerDatesService;
import mk.ukim.finki.dians.hw2backend.service.PythonScriptService;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "http://192.168.225.84:3000")
public class StockController {

    final IssuerDataService issuerDataService;
    final IssuerDatesService issuerDatesService;
    final PythonScriptService pythonScriptService;
    private final RestTemplate restTemplate = new RestTemplate();

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
        return issuerDataService.getDataByIssuer(issuer);
    }


    @GetMapping("/issuer-dates/{issuer}")
    public Optional<IssuerDates> getIssuerLastDate(@PathVariable String issuer) {
        return issuerDatesService.getLastDateForIssuer(issuer);
    }

    @GetMapping("/fill-data")
    public void checkData() {
        String url = "http://localhost:8000/api/scrape";
        restTemplate.getForObject(url, String.class);
    }
}

