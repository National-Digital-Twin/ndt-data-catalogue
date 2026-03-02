/*
 * SPDX-License-Identifier: Apache-2.0
 *
 * This file is unmodified from its original version developed by Acryl Data, Inc.,
 * and is now included as part of a repository maintained by the National Digital Twin Programme.
 * All support, maintenance and further development of this code is now the responsibility
 * of the National Digital Twin Programme.
 */

import filters.BasePathRedirectFilter
import javax.inject.Inject
import play.api.http.DefaultHttpFilters
import play.api.http.EnabledFilters
import play.api.Logger

/**
 * Custom filter chain: BasePathRedirectFilter first, then Play's enabled filters
 * (including GzipFilter from play.filters.enabled in application.conf).
 * Without including EnabledFilters here, only BasePathRedirectFilter would run
 * and response gzip would never be applied.
 */
class Filters @Inject()(
    basePathRedirectFilter: BasePathRedirectFilter,
    enabledFilters: EnabledFilters
) extends DefaultHttpFilters(basePathRedirectFilter +: enabledFilters.filters: _*) {

  private val logger = Logger(getClass)
  logger.info(
    "HTTP filters enabled: " + (basePathRedirectFilter +: enabledFilters.filters).map(_.getClass.getSimpleName).mkString(", ")
  )
}