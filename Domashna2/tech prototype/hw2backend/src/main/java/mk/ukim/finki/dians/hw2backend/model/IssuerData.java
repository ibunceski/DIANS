package mk.ukim.finki.dians.hw2backend.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@Table(name = "issuer_data")
@AllArgsConstructor
@Data
@NoArgsConstructor
@IdClass(IssuerDataKey.class)
public class IssuerData {

    @Id
    private String issuer;
    @Id
    private LocalDate date;

    private String lastTradePrice;
    private String maxPrice;
    private String minPrice;
    private String avgPrice;
    private String percentChange;
    private String volume;
    private String turnoverBest;
    private String totalTurnover;
}