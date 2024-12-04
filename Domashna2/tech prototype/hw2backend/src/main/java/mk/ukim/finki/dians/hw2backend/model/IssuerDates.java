package mk.ukim.finki.dians.hw2backend.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@Data
@Table(name = "issuer_dates")
@AllArgsConstructor
@NoArgsConstructor
public class IssuerDates {

    @Id
    private String issuer;

    private LocalDate lastDate;
}
