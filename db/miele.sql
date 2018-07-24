\c miele;

DROP TABLE IF EXISTS data;
DROP TABLE IF EXISTS loginattempts;

CREATE TABLE data (
  uid           serial   NOT NULL,
  descr        text     NOT NULL,
  ip_address    text     NOT NULL,
  username      text     NOT NULL,
  password      text     NOT NULL,
  PRIMARY KEY (uid)
);

INSERT INTO data (descr,ip_address,username, password) values
    ('File Directory Login','148.100.116.135:8080/listDIR','administrator', 'x'),
    ('production VM','54.68.90.140','root','myw3bsever');

CREATE TABLE loginattempts (
  lid         serial      NOT NULL,
  time_stamp  timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  username    text        NOT NULL,
  password    text        NOT NULL,
  ip_address  text        NOT NULL,
  PRIMARY KEY (lid)
);
