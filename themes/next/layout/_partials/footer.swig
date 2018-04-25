<div class="copyright" >
  {% set current = date(Date.now(), "YYYY") %}
  &copy; {% if theme.since and theme.since != current %} {{ theme.since }} - {% endif %}
  <span itemprop="copyrightYear">{{ current }}</span>
  <span class="with-love">
    <i class="fa fa-heart" style="color: #fc6423;"></i>
  </span>
  <span class="author" itemprop="copyrightHolder"><a href="https://xuanfong1.github.io/">{{ config.author }}</a></span>
  &
  <span ><a href="https://pages.coding.me" style="font-weight: bold">Coding Pages</a></span>
</div>
