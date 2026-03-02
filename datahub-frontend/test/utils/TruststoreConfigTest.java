/*
 * SPDX-License-Identifier: Apache-2.0
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */
package utils;

import static org.junit.jupiter.api.Assertions.*;

import com.typesafe.config.Config;
import com.typesafe.config.ConfigFactory;
import java.util.List;
import org.junit.jupiter.api.Test;

class TruststoreConfigTest {

  @Test
  void fromConfig_missingClientSslEnabledProtocols_usesDefault() {
    Config config =
        ConfigFactory.parseString(
            "metadataService.useSsl = true\n"
                + "metadataService.truststore.path = /path\n"
                + "metadataService.truststore.password = secret\n");
    TruststoreConfig ts = TruststoreConfig.fromConfig(config);
    assertEquals(ConfigUtil.DEFAULT_CLIENT_SSL_ENABLED_PROTOCOLS, ts.sslEnabledProtocols);
  }

  @Test
  void fromConfig_clientSslEnabledProtocolsSet_parsesCommaDelimited() {
    Config config =
        ConfigFactory.parseString(
            "metadataService.useSsl = true\n"
                + "metadataService.truststore.path = /path\n"
                + "metadataService.truststore.password = secret\n"
                + "metadataService.clientSslEnabledProtocols = \"TLSv1.3,TLSv1.2\"\n");
    TruststoreConfig ts = TruststoreConfig.fromConfig(config);
    assertEquals(List.of("TLSv1.3", "TLSv1.2"), ts.sslEnabledProtocols);
  }
}
